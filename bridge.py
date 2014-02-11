
import pxssh
import re

COMMAND_LINE = re.compile(r"fmvalente@login-hpc-01 .*\]\$")

class Bridge:



	def __init__(self):
		try:
			self.ssh = pxssh.pxssh()
			self.ssh.login("login-hpc.ceta-ciemat.es","fmvalente")
			
			fout = file('mylog.txt','w')
			self.ssh.logfile = fout

			#self.ssh.logout()


		except pxssh.ExceptionPxssh as e:
			print("ssh login failure.")
			print(e)



	def modules(self):
		self.ssh.sendline("ls --color=never agent/modules")
		self.ssh.prompt()
		files = self.ssh.before.split()[3:] #first 3 splits are ls and --color path
		print(files)
		return self.ssh.before
			

	def jobs(self):
		self.ssh.sendline("sinfo")
		self.ssh.prompt()
		print(self.ssh.before)
		return self.ssh.before


	def scheduleWorkflow(self):
		self.ssh.sendline("sinfo")
		self.ssh.prompt()
		print(self.ssh.before)
		return self.ssh.before

	def workflows(self):
		self.ssh.sendline("ls agent/workflows --color=never")
		self.ssh.prompt()
		print(self.ssh.before)
		return self.ssh.before


	

if __name__ == "__main__":
	x = Bridge()
	print(x.modules())
	print(x.jobs())
	print(x.scheduleWorkflow())
	print(x.workflows())

	print("thats it")











