
import sys
import subprocess
import glob
import logging
import shelve
from workflow import Workflow
import settings


logging.basicConfig(filename='agent.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')




class Agent(object):
	
	"""Implements job monitoring"""
	def __init__(self, persistent_state):
		sys.path = [sys.path, settings.modules_path]
		self.state = persistent_state
		self.init_persistent_state()


	def init_persistent_state(self):		
		if(not 'id_counter' in self.state):
			self.state['id_counter'] = 0


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

	def id_increment_and_get(self):
		self.state['id_counter'] += 1
		return self.state['id_counter']


if __name__ == "__main__":
	logging.info("called agent with: "+repr(sys.argv))

	#adds module and workflow directories to python's search path
	sys.path.append(settings.agent_path)
	sys.path.append(settings.modules_path)
	sys.path.append(settings.workflows_path)

	persistent_state = shelve.open(settings.persistent_state_path, writeback=True)

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
				flow = Workflow(agent.id_increment_and_get(), sys.argv[i+1])
				flow.launch()
				print(flow.id)
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











