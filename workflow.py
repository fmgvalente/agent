import logging
import settings
import os
import sys
import glob


def from_id(id):
    flow_name = os.path.basename(os.path.normpath(glob.glob( settings.execution_path+'/*_'+str(id) )[0] ))
    logging.info("running workflow {}".format(flow_name))
    name = flow_name.split('_')[0]
    flow_id = flow_name.split('_')[1]
    return Workflow(flow_id, name)


class Workflow:

    def __init__(self, job_id, workflow_name, running=False):
        logging.info("init workflow: {} running={} and id:{}".format(workflow_name, running, job_id))
        self.id = job_id
        self.name = workflow_name
        self.is_running = running
        self.base_path = settings.execution_path+"/{}_{}/".format(self.name, self.id)

        #load module
        try:
            logging.info("loading workflow:" + self.name)
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
        return "workflow "+self.name+" id:"+str(self.id)+" running? "+str(self.is_running)

    def __str__(self):
        return "workflow "+self.name+" id:"+str(self.id)+" running? "+str(self.is_running)

    def launch(self):
        logging.info("launching:" + str(self))
        if(self.is_running):
            raise Exception("Workflow "+self.name+" is already running! Its id is:{}".format(self.id))

        self.prepare_modules()

        #get ready to fire actors
        modules_ready_to_fire = self.get_ready_to_fire()

        #dispatch them
        print("ready_to_fire:")
        for mod in modules_ready_to_fire:
            print(repr(mod))
            mod.launch(self.base_path+mod.module_name+"_"+str(mod.id))

        print("ended ready_to_fire:")

        self.is_running = True
        return self.id

    def updateModules(self):
        for mod in self.all_modules():
            mod.updateState(self.base_path+mod.module_name+"_"+str(mod.id))




    def updateState(self):
        self.updateModules()

        #get ready to fire actors
        modules_ready_to_fire = self.get_ready_to_fire()

        #dispatch them
        print("ready_to_fire:")
        for mod in modules_ready_to_fire:
            print(mod.module_name)
            mod.launch(self.base_path+mod.module_name+"_"+str(mod.id))
        print("ended ready_to_fire:")

    def initialize_persistent_data(self):
        os.makedirs(self.base_path, exist_ok=True)

        #for each task create a directory in the pending list
        print("building directories")
        for mod in self.all_modules():
            print(mod)
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

            if(ready):
                ready_to_fire_nodes.append(mod)

        return ready_to_fire_nodes

    def prepare_modules(self):
        print(repr(self.flow))
        print(dir(self.flow))

    def all_modules(self):
        mod_list = []
        open_list = [self.flow.init]

        while open_list:
            for m in open_list[:]:
                if m not in mod_list:
                    print(m.module_name)
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



