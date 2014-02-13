import module


class Workflow:

	def __init__(self, workflow_name):
		self.name = workflow_name
		self.job_id = None

	def schedule(self):
		self.job_id = 123

	def progress(self):
		return 0.0


if __name__ == "__main__":
	print("testing workflow")
	x = Workflow("test")
	#x.run()
	#x.collect()



