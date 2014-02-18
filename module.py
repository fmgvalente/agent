import sys
import os

class Module:

	def __init__(self, module_name):
		self.module_name = module_name
		self.links = []
		try:
			self.mod = __import__(self.module_name)
		except Exception as e:
			print("failure importing module {}".format(self.module_name))
			print(e)


	def run(self, output_dir_path):
		self.output_dir_path = output_dir_path
		self.enforce_directory_structure(output_dir_path)
		self.mod.launch(self.output_dir_path)

	#call_plugin("example", 1234)
	def enforce_directory_structure(self, directory):
		os.makedirs(directory, exist_ok=True)

	def __rshift__(self, other):
		other.links.append(self)


if __name__ == "__main__":
	sys.path.append("modules")
	print("testing module loading")
	x = Module("feature_extraction")
	x.run("output")



