class Host():
	def __init(self):
		if("ip_address" in data):
			log.write("connect to source using IP: " + data["ip_address"], "debug")
			self.host = data["ip_address"]
		elif("hostname" in data):
			log.write("connect to source using hostname " + data["hostname"], "debug")
			self.host = data["hostname"]
		else:
			log.write("error no ip and hostname passed","error")
			return False
		return True