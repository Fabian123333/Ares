from core import log

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

	def setCredential(self, data):
		print(data)
