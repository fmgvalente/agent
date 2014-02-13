
import sys
import subprocess
import glob
import os
import logging


#general configuration
modules_path = os.path.dirname(os.path.realpath(__file__))+"/modules"
workflows_path = os.path.dirname(os.path.realpath(__file__))+"/workflows"

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
	log = logging.getLogger(__name__)

	agent = Agent()

	i = 1
	while i < len(sys.argv):
		if(sys.argv[i] == "-m"):
			log.info("called agent with -m (request modules)")
			for item in agent.modules():
				print(item)
			i+=1
			continue

		if(sys.argv[i] == "-w"):
			log.info("called agent with -w (request workflows)")
			for item in agent.workflows():
				print(item)
			i+=1
			continue

		if(sys.argv[i] == "-s" and i+1 < len(sys.argv)):
			log.info("called agent with -s (schedule workflow):"+argv[i+1])
			for item in agent.workflows():
				print(item)
			i+=2
			continue


		log.info("called with no parameters, or wrong parameters:")
		log.info(sys.argv)















