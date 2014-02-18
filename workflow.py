import module
import logging
import settings
import os
import sys


def running_workflow_from_id(id):
	pass


class Workflow:

	def __init__(self, job_id, workflow_name, running=False):
		logging.info("init workflow:"+workflow_name+"running={} and id:{}".format(running,job_id))
		self.id = job_id
		self.name = workflow_name
		self.is_running = running

		#load module
		try:
			logging.info("loading module:" + self.name)
			self.flow = __import__(self.name)
		except Exception as e:
			logging.error("failure importing module {}".format(self.name))
			logging.error(e)
			raise


	def progress(self):
		return 0.0

	def __repr__(self):
		return "workflow "+self.name+" id:"+str(self.id)+" running? "+str(self.is_running)

	def __str__(self):
		return "workflow "+self.name+" id:"+str(self.id)+" running? "+str(self.is_running)

	def launch(self):
		if(self.is_running):
			raise Exception("Workflow "+self.name+" is already running! Its id is:{}".format(self.id))

		#initialize running directory
		self.initialize_directory_structure()
		
		#get ready to fire actors
		modules_ready_to_fire = self.flow.


		#dispatch them




		self.is_running = True
		return self.id



	def initialize_directory_structure(self):
		if(self.is_running):
			return;
		os.makedirs(settings.execution_path+"/task_{}".format(self.id), exist_ok=True)
		os.makedirs(settings.execution_path+"/task_{}/running".format(self.id), exist_ok=True)
		os.makedirs(settings.execution_path+"/task_{}/pending".format(self.id), exist_ok=True)
		#for each task create a directory in the pending list
		





if __name__ == "__main__":
	import sys
	sys.path.append(settings.workflows_path)
	print(sys.path)
	print("testing workflow")
	flow = Workflow(666,"test")
	print(flow)
	id = flow.launch()
	print(flow)
	print(id)
	#x.run()
	#x.collect()



