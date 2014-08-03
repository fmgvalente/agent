import sys
import logging
import glob
import os

class Module:

    def __init__(self, module_name, id, **keywords):
        self.module_name = module_name
        self.id = id
        self.mod = None
        
        self.output_modules = []
        self.input_modules = []
        self.input_channels = []

        self.workdir = None
        self.is_running = False
        self.has_finished = False

        self.options = keywords

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
                self << dependency
            self.options.pop("input", None) #removes from options, since it has already been dealt with

    # asks the script attached to this module to give us a script
    # that script is ready to be launched on the grid
    def execution_script(self):
        logging.info("creating execution script for: "+self.module_name)
        return self.mod.create_execution_script(workdir=self.workdir, input=self.input_modules, channel=self.input_channels, **self.options)

    def data(self, channel, **options):
        return self.mod.data(self.workdir, channel, **options)

    def __rshift__(self, other):
            other.input_modules.append(self)
            other.input_channels.append(0)
            self.output_modules.append(other)

    def __lshift__(self, other):
        if isinstance(other, dict):
            self.input_modules.append(other['module'])
            self.input_channels.append(other['channel'])
            other['module'].output_modules.append(self)
        else:
            self.input_modules.append(other)
            self.input_channels.append(0)
            other.output_modules.append(self)


    def __repr__(self):
        return "Module:"+str(self.module_name)+" id="+str(self.id)+" finished:"+str(self.has_finished) + " "+str(self.workdir)

    def __str__(self):
        retstr = repr(self)
        retstr += "\n\tin:" + str(self.input_modules)
        retstr += "\n\tin_ports:" + str(self.input_channels)
        retstr += "\n\tout:"+ str(self.output_modules)
        retstr += "\n-----"+self.module_name+"-----\n"
        return retstr

    def __getitem__(self, index):
        x = {
            'channel' : index,
            'module' : self
        }
        return x



if __name__ == "__main__":
    sys.path.append("modules")
    print("testing module loading")
    x = Module("void",33,input=[Module("zeca",79,input=[]),Module("poca",69)])
    print(x)
    #x.launch("test")
