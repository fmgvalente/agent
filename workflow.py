import logging
import settings
import os
import sys
import glob


def from_id(id):
    flow_name = glob.glob(settings.execution_path+'/*_'+str(id))
    print("running workflows {}", flow_name)
    


    pass


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
            mod.launch(self.base_path+mod.name)
        print("ended ready_to_fire:")

        self.is_running = True
        return self.id

    def updateState(self):
        #get ready to fire actors
        modules_ready_to_fire = self.get_ready_to_fire()


        #dispatch them
        print("ready_to_fire:")
        for mod in modules_ready_to_fire:
            print(repr(mod))
            mod.launch(self.base_path+mod.name)
        print("ended ready_to_fire:")

    def initialize_persistent_data(self):
        if(self.is_running):
            return
        os.makedirs(self.base_path, exist_ok=True)
        
        #for each task create a directory in the pending list
        print("building directories")
        for mod in self.all_modules():
            print(mod)



    def get_ready_to_fire(self):
        #get init
        if(self.is_running is False):
            return [self.flow.init]

        check_list = [self.flow.init]
        get_ready_to_fire_nodes = []

        for mod in check_list:
            if(mod.has_finished):
                check_list += mod.output_modules
                print(check_list)

        return []


    def prepare_modules(self):
        print(repr(self.flow))
        print(dir(self.flow))

    def all_modules(self):
        mod_list = []
        open_list = [self.flow.init]


        while open_list:
            for m in open_list[:]:
                if m in mod_list is False:
                    mod_list.append(m)
                open_list + m.output_modules
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



