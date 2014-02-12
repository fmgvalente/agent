
import sys
import subprocess
import glob

class Agent(object):
	
	"""Implements job monitoring"""
	def __init__(self):
		print("initializing agent")
		sys.path = [sys.path,"./modules"]
		
	def modules(self):
		modules = glob.glob('modules/*.py')
		return [x[8:-3] for x in modules]

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
	print ("running agent:")
	x = Agent()
	print("modules:")
	print(x.modules())
	print("workflows:")
	print(x.workflows())
	print("datasets:")
	print(x.datasets())


















