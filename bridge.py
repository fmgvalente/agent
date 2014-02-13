
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
#
#
#
#
#


class Bridge:

	def __init__(self):
		try:
			self.ssh = pxssh.pxssh()
			self.ssh.login(remote_host,remote_login)
			
			#fout = file('mylog.txt','w')
			#self.ssh.logfile = fout

			#self.ssh.logout()


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
		self.ssh.sendline(agent+"-w "+workflow_name)
		self.ssh.prompt()
		return self.ssh.before


if __name__ == "__main__":

	logging.getLogger(__name__)
	bridge = Bridge()

	print("listing modules:")
	print(bridge.modules())

	print("listing workflows:")
	print(bridge.workflows())

	bridge.scheduleWorkflow(bridge.workflows()[0])











