import module


class workflow:

	def schedule(self, workflow_name):
		pass

	def progress(self):
		return 0.0


if __name__ == "__main__":
	print("testing workflow")
	x = workflow("feature_extraction")
	x.run()
	x.collect()



