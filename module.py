import sys
import os

class Module:

	def __init__(self, module_name):
		self.module_name = module_name
		self.output_modules = []
		self.input_modules = []

		try:
			self.mod = __import__(self.module_name)
		except Exception as e:
			logging.error("failure importing module {}".format(self.module_name))
			logging.exception(e)
			raise Exception("failure importing module, check log")


	def launch(self, output_dir_path):
		self.output_dir_path = output_dir_path
		os.makedirs(self.output_dir_path, exist_ok=True)
		self.mod.launch(self.output_dir_path)

	def collect(self):
		pass

	def __rshift__(self, other):
		other.input_modules.append(self)
		self.output_modules.append(other)


if __name__ == "__main__":
	sys.path.append("modules")
	print("testing module loading")
	x = Module("void")
	x.launch("test")



