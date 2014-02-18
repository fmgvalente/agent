
import pxssh
import re
import logging



#	config

remote_host = "login-hpc.ceta-ciemat.es"
remote_login = "fmvalente"
agent = "python agent/agent.py "
#
#
#

COMMAND_LINE = re.compile(r"fmvalente@login-hpc-01 .*\]\$")


#	Comm gateway with grid
#	TODO: cache responses


class Bridge:

	def __init__(self):
		try:
			self.ssh = pxssh.pxssh()
			self.ssh.login(remote_host,remote_login)

		except pxssh.ExceptionPxssh as e:
			print("ssh login failure.")
			print(e)

	def modules(self):
		self.ssh.sendline(agent+"-m")
		self.ssh.prompt()
		files = self.ssh.before.split()[3:] #first 3 splits are python aget.py -m
		return files

	def workflows(self):
		self.ssh.sendline(agent+"-w")
		self.ssh.prompt()
		files = self.ssh.before.replace(".py", "").split()[3:] #first 3 splits are ls --color path
		return files

	def scheduleWorkflow(self, workflow_name):
		self.ssh.sendline(agent+"-s "+workflow_name)
		self.ssh.prompt()
		try:
			int(self.ssh.before) #may throw, by design
		except Exception as e:
			logging.error("scheduling workflow: "+workflow_name)
			logging.exception(e)
			raise Exception("grid has not returned a valid task id")


if __name__ == "__main__":

	bridge = Bridge()

	print("listing modules:")
	print(bridge.modules())

	print("listing workflows:")
	print(bridge.workflows())

	print ("scheduling workflow: test")
	id = bridge.scheduleWorkflow("test")
	print(id)











