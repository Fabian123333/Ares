import os

from core import log
import paramiko
import select

class HostTemplate():
	def __init__(self, conf):
		self.conf = conf
		
		ip_address = self.conf.getIPAdress()
		hostname = self.conf.getHostname()
		
		if ip_address:
			log.write("connect to source using IP: " + ip_address, "debug")
			self.host = ip_address
		elif fqdn:
			log.write("connect to source using hostname: " + hostname, "debug")
			self.host = hostname
		else:
			log.write("error no ip and hostname passed","error")
			return False

		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)

	def setCredential(self, cred):
		if(not cred.getType()):
			log.write("error no type specified for credentials", "error")
			return False
		
		if(cred.getType() == "certificate"):
			log.write("deploy private key")
			with open("/id_rsa", "w+") as fh:
				fh.write(cred.getSecret())
			os.chmod("/id_rsa", 0o600)
		elif(cred.getType() == "password"):
			self.secret = cred.getSecret()
		else:
			log.write("error unsupported credential type: " + cred.getType())
			return False
		
		self.username = cred.getUsername()
		self.secret_type = cred.getType()

	def isConnected(self):
		try:
			self.client.get_transport()
		except:
			return False
		return True

	def connect(self):
		log.write("try to connect to host: " + self.host, "notice")
		if(self.secret_type == "password"):
			self.client.connect(self.host, username=self.username, password=self.secret)
			log.write("connected by password", "debug")
			return True
		elif(self.secret_type == "certificate"):
			self.client.connect(self.host, username=self.username, key_filename="/id_rsa")
			log.write("connected by certificate", "debug")
			return True
		else:
			log.write("secret type not supported by host_linux: " + self.secret_type)
#		except:
#			log.write("host not reachable: " + self.host)
			return False
			
	def writeBinary(self, data):
		return self.stdin.write(data)
			
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
		
		if not self.isConnected():
			self.connect()
		
		log.write("execute command: " + cmd, "debug")
		
		self.transport = self.client.get_transport()
		self.channel = self.transport.open_session()
		self.channel.exec_command(cmd)

	def fileExists(self, path):
		cmd = 'stat "' + path + '"'
		stdin, stdout, ssh_stderr = self.client.exec_command(cmd)
		if ssh_stderr:
			return False
		return True

	def createDirectoryRecursive(self, path):
		cmd = 'mkdir -p "' + path + '"'
		stdin, stdout, ssh_stderr = self.client.exec_command(cmd)

		return True
		
	def closeFile(self):
		self.stdin.flush()
		self.stdin.channel.shutdown_write()

	def syncDirectory(self, source=None, target="/", delete=False):
		if source == None:
			source = self.tmp_path
	
		cmd = "rsync -a " + source + " " + target
		
		if delete == True:
			cmd += " -delete"
		
		log.write("execute command: " + cmd)
		
		stdin, stdout, ssh_stderr = self.client.exec_command(cmd)
		return True

	def restoreArchive(self):
		self.tmp_path = "/tmp/ares-tmp/"
		
		cmd = "tar -C " + self.tmp_path + " -xz "
		
		if not self.fileExists(self.tmp_path):
			self.createDirectoryRecursive(self.tmp_path)

		log.write("execute command: " + cmd, "debug")

		self.stdin, self.stdout, self.stderr = self.client.exec_command(cmd)

# Optional Stuff if target supports docker

	def getContainersByName(self, name):
		cmd = 'docker ps -q --filter "name=' + name + '"'
		
#		log.write("execute command: " + cmd, "debug")
		stdin, stdout, ssh_stderr = self.client.exec_command(cmd)

		ids = str(stdout.read(), 'ascii').splitlines()
		
		return ids
	
	def createArchiveFromContainerId(self, id: str):
		cmd = 'docker run --rm --volumes-from "' + id + '" debian bash -c \'mount | grep -vE "type (proc|cgroup|(tmp|sys)fs|mqueue|devpts)" | grep -vE "/etc/(resolv.conf|host(name|s))" | grep -v "overlay on /" | awk "{print ($3)}" | xargs tar -Ocz\''
		
#		log.write("execute command: " + cmd, "debug")
		self.transport = self.client.get_transport()
		self.channel = self.transport.open_session()
		self.channel.exec_command(cmd)		
	
	def getContainersByStack(self, name):
		cmd = "docker stack ps --no-trunc " + name + " |awk '$6 ~ \"Running\" {print $2}' | uniq"
		
#		log.write("execute command: " + cmd, "debug")
		stdin, stdout, ssh_stderr = self.client.exec_command(cmd)
		
		names = str(stdout.read(), 'ascii').splitlines()

		return names