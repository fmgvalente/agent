import module
import logging

class Workflow:

	def __init__(self, workflow_name, job_id):
		logging.info("init workflow:"+workflow_name)
		self.name = workflow_name
		self.job_id = job_id

	def progress(self):
		return 0.0

	def __repr__(self):
		return "workflow "+self.name+" id:"+str(self.job_id)

	def __str__(self):
		return "workflow "+self.name+" id:"+str(self.job_id)


if __name__ == "__main__":
	print("testing workflow")
	x = Workflow("test",666)
	print(x)
	#x.run()
	#x.collect()



