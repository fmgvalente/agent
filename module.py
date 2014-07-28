import sys
import logging
import glob
import os

class Module:

    def __init__(self, module_name, id, **keywords):
        self.module_name = module_name
        self.id = id
        self.output_modules = []
        self.input_modules = []
        self.workflow_dir = None
        self.is_running = False
        self.has_finished = False
        self.mod = None
        self.channel = -1    #specifies which of the output ports is used to obtain data
        self.maps = {}

        #checks for module existence
        try:
            self.mod = __import__(self.module_name, globals(), locals())
        except Exception as e:
            excstr = "failure importing module {}".format(self.module_name)
            raise Exception(excstr)

        #obtains an input=* optional argument and adds it to its list of dependencies
        #this is convinient when creating workflows by hand
        if 'input' in keywords:
            for dependency in keywords['input']:
                dependency >> self

    # asks the script attached to this module to give us a script
    # that script is ready to be launched on the grid
    def create_execution_script(self):
        logging.info("creating execution script for: "+self.module_name)
        return self.mod.create_execution_script()

    def data(self):
        pass

    def __rshift__(self, other):
        other.input_modules.append(self)
        self.output_modules.append(other)

    def __repr__(self):
        return "Module:"+self.module_name+" id="+str(self.id)+" channel:"+str(self.channel)+" finished:"+str(self.has_finished)+"\n\t"

    def __str__(self):
        retstr = repr(self)
        retstr += "\n\tin:" + str(self.input_modules)
        retstr += "\n\tout:"+ str(self.output_modules)
        retstr += "\n-----"+self.module_name+"-----\n"
        return retstr

    # def __getitem__(self, index):
    #     copyModule = Module(self.module_name, self.id)
    #     copyModule.output_modules = self.output_modules
    #     copyModule.input_modules = self.input_modules
    #     copyModule.workflow_dir = self.workflow_dir
    #     copyModule.is_running = self.is_running
    #     copyModule.has_finished = self.has_finished
    #     copyModule.mod = self.mod
    #     copyModule.channel = index    #specifies which of the output ports is used to obtain data
    #     return copyModule

    def __getitem__(self, index):
        #self.maps
        return self


if __name__ == "__main__":
    sys.path.append("modules")
    print("testing module loading")
    x = Module("void",33,input=[Module("zeca",79,input=[]),Module("poca",69)])
    print(x)
    #x.launch("test")
