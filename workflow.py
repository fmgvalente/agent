import module
import logging




def running_workflow_from_id(id):
	pass


class Workflow:

	def __init__(self, job_id, workflow_name, running=False):
		logging.info("init workflow:"+workflow_name)
		self.id = job_id
		self.name = workflow_name
		self.is_running = running


	def progress(self):
		return 0.0

	def __repr__(self):
		return "workflow "+self.name+" id:"+str(self.id)+" running? "+str(self.is_running)

	def __str__(self):
		return "workflow "+self.name+" id:"+str(self.id)+" running? "+str(self.is_running)

	def launch(self):
		print("I wish I could launch...")
		self.is_running = True
		return self.id


if __name__ == "__main__":
	print("testing workflow")
	flow = Workflow(666,"test")
	print(flow)
	id = flow.launch()
	print(flow)
	print(id)
	#x.run()
	#x.collect()



