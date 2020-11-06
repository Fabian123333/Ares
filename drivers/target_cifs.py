from core import log
import fs, os

class TargetTemplate():
	def __init__(self, conf):
		self.conf = conf
		
		ip_address = self.conf.getIPAdress()
		fqdn = self.conf.getFQDN()
		
		if ip_address:
			log.write("connect to target using IP: " + ip_address, "debug")
			self.host = ip_address
		elif fqdn:
			log.write("connect to target using FQDN: " + fqdn, "debug")
			self.host = fqdn
		else:
			log.write("error no ip and fqdn passed","error")
			return False
			
		self.path = self.conf.path
		self.fs = None

	def setCredential(self, credential):
		if(not credential.getType()):
			log.write("error no type specified for credentials", "error")
		
		if(not credential.getType() == "password"):
			log.write("error cifs only supports password auth", "error")
			return False
			
		self.secret_type = credential.getType()
		
		self.secret = credential.getSecret()
		self.username = credential.getUsername()

	def connect(self):
		log.write("estabish connection", "debug")
		if(self.secret_type == "password"):
			self.fs = fs.open_fs('smb://%s:%s@%s/%s' % (self.username, self.secret, self.host, self.conf.location))
			if(not self.fs.exists(self.conf.path)):
				log.write("create backup dir: " + self.conf.path, "info")
				self.fs.makedir(self.conf.path)
		else:
			log.write("unsupported secret type", "error")

	def fileExists(self, path):
		abs_path = self.path + "/" + path
		if(self.fs.exists(abs_path)):
			return True
		else:
			return False
	
	def openFile(self, path, mode="wb"):
		abs_path = self.path + "/" + path
		log.write("open target file: "+abs_path, "debug")
		if(self.fileExists(abs_path)):
			log.write("cannot create backup, file exists: ".abs_path)
			return False
		self.fh = self.fs.open(abs_path, mode)

	def deleteFile(self, path):
		abs_path = self.path + "/" + path
		if(not self.fileExists(path)):
			return False
		
		log.write("delete file: " + path)
		return self.fs.remove(abs_path)

	def readBinary(self):
		return self.fh.read()

	def writeFile(self, data):
		self.fh.write(data)

	def closeFile(self):
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
