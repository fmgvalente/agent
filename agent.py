
import sys
import subprocess
import glob
import os
import logging
import workflow


#general configuration
agent_path = os.path.dirname(os.path.realpath(__file__))
modules_path = os.path.dirname(os.path.realpath(__file__))+"/modules"
workflows_path = os.path.dirname(os.path.realpath(__file__))+"/workflows"
logging.basicConfig(filename='agent.log',level=logging.DEBUG)




class Agent(object):
	
	"""Implements job monitoring"""
	def __init__(self):
		sys.path = [sys.path, modules_path]
		
	def modules(self):
		modules = glob.glob(modules_path+'/*.py')
		return [x[len(modules_path)+1:-3] for x in modules]

	def workflows(self):
		work = glob.glob(workflows_path+'/*.py')
		return [x[len(workflows_path)+1:-3] for x in work]


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

	def signal_state_change():
		pass


if __name__ == "__main__":
	logging.info("called agent with: "+repr(sys.argv))
	agent = Agent()

	i = 1
	while i < len(sys.argv):
		if(sys.argv[i] == "-m"):
			logging.info("called agent with -m (request modules)")
			for item in agent.modules():
				print(item)
			i+=1
			continue

		if(sys.argv[i] == "-w"):
			logging.info("called agent with -w (request workflows)")
			for item in agent.workflows():
				print(item)
			i+=1
			continue

		if(sys.argv[i] == "-s" and i+1 < len(sys.argv)):
			logging.info("called agent with -s (schedule workflow):"+sys.argv[i+1])
			
			#creates workflow
			flow = workflow(argv[i+1])
			i+=2
			continue


		logging.info("wrong parameters?")
		logging.info(sys.argv[i])
		quit()















