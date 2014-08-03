import os
import sys

#loads a file, the type of which is specified by the argument options
#"harmonizes" it to a table format that is common throughout the scripts
def create_execution_script(**options):
	#settings = __import__(self.name, globals(), locals())
	import settings;
	dataset_path = settings.dataset_path
	script_string = "python " + os.path.realpath(__file__) 
	script_string += " "+options['type']+" "+dataset_path+"/"+options['src']+" "+ repr(options['field']) 
	script_string += " "+options['workdir']

	#we wont be using this, its inserted as part of a transformation of this script
	#by the workflow object (it inserts some more commands in order to do distributed book keeping)
    #script = "#!/bin/sh\n"

	return script_string


#returns something out of the results of script execution
def data(workdir, **options):
	import numpy as np
	return {
		'datatype': 'dataset',
		'data': np.load(workdir+"/data_array.npy"),
		'target': np.load(workdir+"/target.npy"),
		}

if __name__ == "__main__":
	import numpy as np
	import math
	type = sys.argv[1]
	path = sys.argv[2]
	coln = sys.argv[3]
	workdir = sys.argv[4]



	if type in 'csv':

		#this converts NaNs into zero, ugly hack
		converterDict = dict(map(lambda s: (s, lambda x: 0.0 if math.isnan(float(x)) else float(x)), range(44)))
		data = np.loadtxt(open(path,"rb"),delimiter=",",skiprows=1, converters=converterDict)
		target = np.ravel(data[:, [coln]])

		np.save(workdir+"/data_array", data)
		np.save(workdir+"/target", target)

	else:
		print("not implemented")
		print(type)
