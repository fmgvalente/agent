import module
import logging

class Workflow:

	def __init__(self, workflow_name, job_id):
		logging.info("init workflow:"+workflow_name)
		self.name = workflow_name
		self.job_id = job_id

	def progress(self):
		return 0.0


if __name__ == "__main__":
	print("testing workflow")
	x = Workflow("test",666)
	#x.run()
	#x.collect()



