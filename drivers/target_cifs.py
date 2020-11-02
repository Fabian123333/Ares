from core import log
import fs, os

class Target():
	def __init__(self, data):
		if("ip_address" in data):
			log.write("connect to target using IP: " + data["ip_address"], "debug")
			self.host = data["ip_address"]
		elif("fqdn" in data):
			log.write("connect to target using FQDN: " + data["fqdn"], "debug")
			self.host = data["fqdn"]
		else:
			log.write("error no ip and fqdn passed","error")
			return False
		
		self.path = data["path"]
		self.location = data["location"]
		self.fs = None

	def setCredential(self, data):
		if(not "type" in data):
			log.write("error no type specified for credentials", "error")
		
		if(not data["type"] == "password"):
			log.write("error cifs only supports password auth", "error")
			return False
			
		self.secret_type = data["type"]
		
		self.secret = data["secret"]
		self.username = data["username"]

	def connect(self):
		log.write("estabish connection", "debug")
		if(self.secret_type == "password"):
			self.fs = fs.open_fs('smb://%s:%s@%s/%s' % (self.username, self.secret, self.host, self.location))
			if(not self.fs.exists(self.path)):
				log.write("create backup dir: " + self.path, "info")
				self.fs.makedir(self.path)
		else:
			log.write("unsupported secret type", "error")

	def fileExists(self, path):
		abs_path = self.path + "/" + path
		if(self.fs.exists(abs_path)):
			return True
		else:
			return False
	
	def openFile(self, path)
		if(self.fileExists(path))
			log.write("cannot create backup, file exists: ".path)
			return False
		self.fh = self.fs.open(path, 'w')

	def writeFile(self, data):
		self.fh.write(data)

	def closeFile(self)
		self.fh.close()

	def createDirectory(self, path):
		abs_path = self.path + "/" + path
		return self.fs.makedir(abs_path)

	def createDirectoryRecursive(self, path):
		rel_path = ""
		for part in path.split("/"):
			rel_path += "/" + part
			if(not self.fileExists(rel_path)):
				self.createDirectory(rel_path)
