
import sys
import subprocess
import glob
import os

#general configuration
modules_path = os.path.dirname(os.path.realpath(__file__))+"/modules"

print (modules_path)

class Agent(object):
	
	"""Implements job monitoring"""
	def __init__(self):
		sys.path = [sys.path, modules_path]
		
	def modules(self):
		modules = glob.glob(modules_path+'/*.py')
		return [x[len(modules_path)+1:-3] for x in modules]

	def workflows(self):
		return glob.glob('workflows/*.py')


	def datasets(self):
		out = subprocess.check_output(["ls", "--color=never", "datasets"])
		files = out.split()
		return files

	def progress(self, job_id):
		return 0.42

	def scheduleWorkflow(self):
		return 42

	def cancelWorkflow():
		pass


if __name__ == "__main__":
	import sys
	agent = Agent()

	for arg in sys.argv:
		if(arg == "-m"): print(agent.modules())


#	print("modules:")
#	print(x.modules())
#	print("workflows:")
#	print(x.workflows())
#	print("datasets:")
#	print(x.datasets())


















