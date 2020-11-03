import os

from core import log
import paramiko
import select

class Host():
	def __init__(self, data):
		if("ip_address" in data and data["ip_address"] != None):
			log.write("connect to source using IP: " + data["ip_address"], "debug")
			self.host = data["ip_address"]
		elif("hostname" in data):
			log.write("connect to source using hostname " + data["hostname"], "debug")
			self.host = data["hostname"]
		else:
			log.write("error no ip and hostname passed","error")
			return False

		self.hostname = data["hostname"]
		self.id = str(data["_id"])

		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)

	def setCredential(self, data):
		if(not "type" in data):
			log.write("error no type specified for credentials", "error")
			return False
		
		if(data["type"] == "certificate"):
			log.write("deploy private key")
			with open("/id_rsa", "w+") as fh:
				fh.write(data["secret"])
			
			os.chmod("/id_rsa", 0o600)
		
		self.secret_type = data["type"]
		
		self.secret = data["secret"]
		self.username = data["username"]

	def connect(self):
		if(self.secret_type == "password"):
			self.client.connect(self.host, username=self.username, password=self.secret)
		elif(self.secret_type == "certificate"):
			self.client.connect(self.host, username=self.username, key_filename="/id_rsa")
		else:
			log.write("secret type not supported by host_linux: " + self.secret_type)
			
	def readBinary(self):
		data = self.channel.recv(8196)
		if data:
			return data
		else:
			return False

	def read(self):
		out = ""
		while True:
			data = self.channel.recv(1024)
			if not data:
				del self.channel
				break
			out += data
		return out

	def createArchiveFromPaths(self, path):
		cmd = "tar -Ocz "
		
		p = ""
		for s in path:
			p += s + "/ "
		
		cmd += p
		
		# log.write("execute command: " + cmd, "debug")
		
		self.transport = self.client.get_transport()
		self.channel = self.transport.open_session()
		self.channel.exec_command(cmd)

# Optional Stuff if target supports docker

	def getContainersByName(self, name):
		cmd = 'docker ps -q --filter "name=' + name + '"'
		
		# log.write("execute command: " + cmd, "debug")
		stdin, stdout, ssh_stderr = self.client.exec_command(cmd)

		ids = str(stdout.read(), 'ascii').splitlines()
		
		return ids
	
	def createArchiveFromContainerId(self, id: str):
		cmd = 'docker run --rm --volumes-from "' + id + '" debian bash -c \'mount | grep -vE "type (proc|cgroup|(tmp|sys)fs|mqueue|devpts)" | grep -vE "/etc/(resolv.conf|host(name|s))" | grep -v "overlay on /" | awk "{print ($3)}" | xargs tar -Ocz\''
		
		# log.write("execute command: " + cmd, "debug")
		self.transport = self.client.get_transport()
		self.channel = self.transport.open_session()
		self.channel.exec_command(cmd)		
	
	def getContainersByStack(self, name):
		cmd = "docker stack ps --no-trunc " + name + " |awk '$6 ~ \"Running\" {print $2}' | uniq"
		
		# log.write("execute command: " + cmd, "debug")
		stdin, stdout, ssh_stderr = self.client.exec_command(cmd)
		
		names = str(stdout.read(), 'ascii').splitlines()

		return names