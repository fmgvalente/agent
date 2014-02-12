
import pxssh
import re



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
		files = self.ssh.before.replace(".py", "").split()[3:] #first 3 splits are python aget.py -m
		return files

	def jobs(self):
		self.ssh.sendline(agent+"-m")
		self.ssh.prompt()
		return self.ssh.before


	def scheduleWorkflow(self):
		self.ssh.sendline(agent+"-m")
		self.ssh.prompt()
		return self.ssh.before

	def workflows(self):
		self.ssh.sendline(agent+"-w")
		self.ssh.prompt()
		files = self.ssh.before.replace(".py", "").split()[3:] #first 3 splits are ls --color path
		return files

if __name__ == "__main__":

	x = Bridge()
	


	print("listing modules:")
	print(x.modules())
	print(type(x.modules()))
	print(len(x.modules()))
	for item in x.modules():
		print(item)
		print(type(item))
	print(x.modules[0])
	z=["a","b"]
	print(z)
	#print(x.jobs())
	#print(x.scheduleWorkflow())
	#print(x.workflows())












