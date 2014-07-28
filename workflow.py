import logging
import settings
import os
import sys
import glob
import subprocess

#once persisted, a workflow has an id, that will correspond to a specific location on disk
#given that id, this method loads the workflow object to memory
def from_id(id):
    flow_name = os.path.basename(os.path.normpath(glob.glob(settings.execution_path+'/*_'+str(id))[0]))
    logging.info("running workflow {}".format(flow_name))
    name = flow_name.split('_')[0]
    flow_id = flow_name.split('_')[1]
    return Workflow(flow_id, name)


class Workflow:

    #creates a new workflow object. requires a unique id and the location of the workflow description file
    def __init__(self, job_id, workflow_name, *flags):
        self.id = job_id
        self.name = workflow_name
        self.base_path = settings.execution_path+"/{}_{}/".format(self.name, self.id)
        self.has_finished = os.path.exists(self.base_path+"/_state_finished")
        logging.info("init workflow: {} finished={} and id:{}".format(workflow_name, self.has_finished, job_id))
        
        #load module
        try:
            self.flow = __import__(self.name, globals(), locals())

            #initialize running directory if not on test mode
            if 'test' not in flags:
                self.initialize_persistent_data()

        except Exception as e:
            logging.error("failure importing workflow {}".format(self.name))
            logging.error(e)
            raise

    def progress(self):
        return 0.0

    def __repr__(self):
        return "workflow "+self.name+" id:"+str(self.id)+" finished: "+str(self.has_finished)

    def __str__(self):
        retstr = repr(self)
        for mod in self.all_modules():
            retstr += "\n\t"+str(mod)
        return retstr;


    def output_dir(self, module):
        return self.base_path+module.module_name+"_"+str(module.id)

    #executes a step on the workflow
    def launch(self):
        logging.info("launching workflow:" + str(self))
        if(self.has_finished):
            logging.error("call launch on a workflow already running: {}".format(self))
            raise Exception("Workflow "+self.name+" has already completed! Its id is:{}".format(self.id))

        #is there something we must do beforehand?
        #currently this does nothing
        self.prepare_modules()

        #lets get the ready to fire actors
        #these are actores/modules with all dependencies fulfilled
        modules_ready_to_fire = self.get_ready_to_fire()

        #dispatches them
        self.updateState()

        #returns a unique identifier for the workflow
        return self.id


    #synchs information stored on the file system with in-memory representation
    def updateModules(self):
        for mod in self.all_modules():
            if(glob.glob(self.output_dir(mod)+'/_state_running')):
                mod.is_running = True

            if(glob.glob(self.output_dir(mod)+'/_state_finished')):
                mod.is_running = False
                mod.has_finished = True

    #helper method that does exactly what the name implies
    def are_all_modules_finished(self):
        for mod in self.all_modules():
            if(not mod.has_finished):
                logging.info("checking for finished mods, this one is unfinished: " + repr(mod))
                return False
        return True


#   updates the workflow state. if it's already finished returns immediately
    def updateState(self):

        if(self.has_finished):
            logging.info("updating workflow {} but it has already finished...".format(self))
            return

        #potentially changes state
        self.updateModules()

        #checks if all jobs have been finished!
        if self.are_all_modules_finished():
            self.has_finished = True
            logging.info("{} completed".format(self))
            file = open(self.base_path+"/_state_finished",'w')
            file.close()
            return

        #get ready to fire actors
        modules_ready_to_fire = self.get_ready_to_fire()
        logging.info("Ready to fire actors:"+str(modules_ready_to_fire))

        #dispatch them
        for mod in modules_ready_to_fire:
            logging.info("ready to fire and firing: {}".format(repr(mod)))
            logging.info(mod.module_name)
            #first we instruct the module to create a script understandable by srun
            #we store it in the proper place on the workflow directory tree
            #also we add some state management functionality
            #we add it to the script so that these ch\nanges ocurr on the child process
            #made by whichever machine executes them
            script_string = "#!/bin/sh\n"
            script_string += "touch {}/_state_running\n".format(self.output_dir(mod))
            script_string += mod.create_execution_script()
            script_string += "touch {}/_state_finished\n".format(self.output_dir(mod))
            #we add an instruction to create an agent update at the end of its execution
            script_string += "agent_watchdog {}\n".format(self.output_dir(mod))

            #stores script in order to pass it to srun
            file = open(self.output_dir(mod)+"/launch.sh",'w')
            file.write(script_string)
            file.close()

            #then we execute that script
            mod.is_running = True
            subprocess.Popen(["sh", self.output_dir(mod)+"/launch.sh"])
            print("DONE: "+mod.module_name)

    def initialize_persistent_data(self):
        os.makedirs(self.base_path, exist_ok=True)

        #for each task create a directory in the pending list
        for mod in self.all_modules():
            os.makedirs(self.output_dir(mod), exist_ok=True)

    #returns a list of nodes in ready to fire state
    #this means they have not yet been scheduled, but all their precedences have been fulfilled
    def get_ready_to_fire(self):
        mods = self.all_modules()
        ready_to_fire_nodes = []

        for mod in mods:
            if(mod.has_finished or mod.is_running):
                continue

            inputs = mod.input_modules
            ready = True
            for input in inputs:
                if(not input.has_finished):
                    ready = False

            if(ready and (mod not in ready_to_fire_nodes)):
                ready_to_fire_nodes.append(mod)

        logging.info(ready_to_fire_nodes)
        return ready_to_fire_nodes

    #executes some init tasks if required
    def prepare_modules(self):
        #logging.info(repr(self.flow))
        #logging.info(dir(self.flow))
        pass

    #returns a list of all nodes in the workflow
    def all_modules(self):
        mod_list = []
        open_list = [self.flow.init]

        while open_list:
            for m in open_list[:]:
                if m not in mod_list:
                    mod_list.append(m)
                open_list = open_list + m.output_modules
                open_list.remove(m)

        return mod_list

#not the main main, mainly for tests
if __name__ == "__main__":
    sys.path.append(settings.workflows_path)
    sys.path.append(settings.modules_path)

    print("testing workflow")
    flow = Workflow(666, "xpto")
    print(flow)
    id = flow.launch()
    print(flow)
    print(id)
    #x.run()
    #x.collect()



