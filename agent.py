
import sys
import subprocess
import glob
import os
import logging
import shelve
from workflow import Workflow


#general configuration
agent_path = os.path.dirname(os.path.realpath(__file__))
modules_path = os.path.dirname(os.path.realpath(__file__))+"/modules"
workflows_path = os.path.dirname(os.path.realpath(__file__))+"/workflows"
persistent_state_filepath = os.path.dirname(os.path.realpath(__file__))+"/persistentstate"

logging.basicConfig(filename='agent.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')




class Agent(object):
	
	"""Implements job monitoring"""
	def __init__(self, persistent_state):
		sys.path = [sys.path, modules_path]
		self.state = persistent_state
		self.init_persistent_state()


	def init_persistent_state(self):
		#self.state = shelve.open(persistent_state_filepath, writeback=True)
		
		
		if(not self.state.has_key('job_id_counter')):
			self.state['job_id_counter'] = 0


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

	#adds module and workflow directories to python's search path
	sys.path.append(agent_path)
	sys.path.append(modules_path)
	sys.path.append(workflows_path)

	persistent_state = shelve.open(persistent_state_filepath, writeback=True)

	agent = Agent(persistent_state)
	try:

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
				flow = Workflow(sys.argv[i+1], state[job_id])
				print(flow.job_id)
				print(repr(flow))
				state[job_id]+=1
				i+=2
				continue


			logging.info("wrong parameters?")
			logging.info(sys.argv[i])
			quit()

	except Exception as e:
		logging.exception(e)
		print("A nasty exception was caught. Check the log for more details...")
		print(e)

	persistent_state.close()











