import sys
import logging
import glob
import os

class Module:

    def __init__(self, module_name, id):
        self.module_name = module_name
        self.id = id
        self.output_modules = []
        self.input_modules = []
        self.workflow_dir = None
        self.is_running = False
        self.has_finished = False
        self.mod = None

        #assumes directory exists
    def launch(self, output_dir):
        self.basepath = output_dir
        try:
            self.mod = __import__(self.module_name, globals(), locals())
        except Exception as e:
            logging.error("failure importing module {}".format(self.module_name))
            logging.exception(e)
            raise Exception("failure importing module {}, check log".format(self.module_name))

        open(self.basepath+"/_state_running", "w")
        self.is_running = True
        self.mod.launch(self.basepath)

    def collect(self):
        pass

    def __rshift__(self, other):
        other.input_modules.append(self)
        self.output_modules.append(other)

    def updateState(self, output_dir):
        if(glob.glob(output_dir+'/_state_running')):
            self.is_running = True

        if(glob.glob(output_dir+'/_state_finished')):
            self.is_running = False
            self.has_finished = True
        

    def __repr__(self):
        return self.module_name+" "+str(self.id)

    def __str__(self):
        return self.module_name+" "+str(self.id)


if __name__ == "__main__":
    sys.path.append("modules")
    print("testing module loading")
    x = Module("void")
    x.launch("test")
