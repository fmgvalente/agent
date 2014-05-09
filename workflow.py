import logging
import settings
import os
import sys
import glob


def from_id(id):
    flow_name = os.path.basename(os.path.normpath(glob.glob(settings.execution_path+'/*_'+str(id))[0]))
    logging.info("running workflow {}".format(flow_name))
    name = flow_name.split('_')[0]
    flow_id = flow_name.split('_')[1]
    return Workflow(flow_id, name)


class Workflow:

    def __init__(self, job_id, workflow_name):
        self.id = job_id
        self.name = workflow_name
        self.base_path = settings.execution_path+"/{}_{}/".format(self.name, self.id)
        self.has_finished = os.path.exists(self.base_path+"/_state_finished")
        logging.info("init workflow: {} finished={} and id:{}".format(workflow_name, self.has_finished, job_id))
        
        #load module
        try:
            self.flow = __import__(self.name, globals(), locals())

            #initialize running directory
            self.initialize_persistent_data()

        except Exception as e:
            logging.error("failure importing workflow {}".format(self.name))
            logging.error(e)
            raise

    def progress(self):
        return 0.0

    def __repr__(self):
        return "workflow "+self.name+" id:"+str(self.id)+" finished? "+str(self.has_finished)

    def __str__(self):
        return "workflow "+self.name+" id:"+str(self.id)+" finished? "+str(self.has_finished)

    def launch(self):
        logging.info("launching:" + str(self))
        if(self.has_finished):
            logging.error("call launch on a workflow already running: {}".format(self))
            raise Exception("Workflow "+self.name+" has already completed! Its id is:{}".format(self.id))

        self.prepare_modules()

        #get ready to fire actors
        modules_ready_to_fire = self.get_ready_to_fire()

        #dispatch them
        for mod in modules_ready_to_fire:
            logging.info("ready to fire and firing: {}".format(repr(mod)))
            mod.launch(self.base_path+mod.module_name+"_"+str(mod.id))

        return self.id

    def updateModules(self):
        for mod in self.all_modules():
            mod.updateState(self.base_path+mod.module_name+"_"+str(mod.id))

    def are_all_modules_finished(self):
        for mod in self.all_modules():
            if(not mod.has_finished):
                return False
        return True


#   updates the workflow state. if its already finished returns immediately
#
#
    def updateState(self):

        if(self.has_finished):
            logging.info("updating workflow {} but it has already finished...".format(self))
            return

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

        #dispatch them
        for mod in modules_ready_to_fire:
            logging.info("ready to fire and firing: {}".format(repr(mod)))
            mod.launch(self.base_path+mod.module_name+"_"+str(mod.id))

    def initialize_persistent_data(self):
        os.makedirs(self.base_path, exist_ok=True)

        #for each task create a directory in the pending list
        for mod in self.all_modules():
            os.makedirs(self.base_path+mod.module_name + "_" + str(mod.id), exist_ok=True)

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

    def prepare_modules(self):
        logging.info(repr(self.flow))
        logging.info(dir(self.flow))

    def all_modules(self):
        mod_list = []
        open_list = [self.flow.init]

        while open_list:
            for m in open_list[:]:
                if m not in mod_list:
                    #print(m.module_name)
                    mod_list.append(m)
                open_list = open_list + m.output_modules
                open_list.remove(m)

        return mod_list


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



