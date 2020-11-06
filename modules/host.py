import json
from pydantic import BaseModel
from typing import Optional

from core.db import DB
from core import log

from modules.credential import Credential

col_name="host"

class Host():
	col_name = "host"

	def __init__(self, id=None, hostname=None, data=None):
		if data == None:
			if(hostname != None and id == None):
				id = self.getIdByName(hostname)
				return
			if(id != None and id != False):
				self.get(id)
				return
		else:
			if id == None:
				self.create(data)
				return

	def update(self, data):
		if not self.exists():
			return False
		
		value = dict()
		for k, v in vars(data).items():
			if v != None:
				value[k] = v

		log.write("update host %s (%s)" % (self.getID(), value))
		update = self.getDB().updateDocByID(self.id, value)
		self.get(self.getID())
		return True


	def getCredentialID(self):
		if(hasattr(self, "credential_id")):
			return self.credential_id
		return False

	def getCredential(self):
		id = self.getCredentialID()
		if id:
			return Credential(self.getCredentialID())
		return False

	def getDB(self):
		return DB(self.col_name)

	def toJSON(self):	
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getIdByName(self, hostname: str):
		print(hostname)
		doc = self.getDB().findOne({"hostname": hostname})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def create(self, data):
		log.write("create host: " + str(data), "debug")
	
		if(Host(hostname=data.hostname).exists()):
			log.write("error host already exists: " + str(data), "debug")
			return False

		log.write("create host: " + str(data))
	
		doc = data.dict()
		return self.getDB().addDoc(doc)

	def getID(self):
		if hasattr(self, "id"):
			return self.id
		else:
			return False

	def exists(self):
		if(hasattr(self, "exist")):
			return self.exist
		return False

	def getIPAdress(self):
		if hasattr(self, "ip_address"):
			return self.ip_address
		return False

	def getName(self):
		if hasattr(self, "name"):
			return self.name
		return False

	def getHostname(self):
		if hasattr(self, "hostname"):
			return self.hostname
		return False

	def getType(self):
		if hasattr(self, "type"):
			return self.type
		return False

	def get(self, id: str):
		log.write("load host by id: " + id, "debug")
		ret = self.getDB().get(id)
		
		if ret:
			for k, v in ret.items():
				setattr(self, k, v)
			self.id = str(ret["_id"])
			del(self._id)
			self.exist = True
		else: 
			return False

	def getAll(self, filter={}, type="object"):
		log.write("get all hosts", "debug")
		docs = self.getDB().getCollection(query=filter)
		
		if(type == "JSON"):
			return docs
		else:
			ret = []
			for d in docs:
				r = Host(str(d["_id"]))
				ret.append(r)
			return ret

	def delete(self):
		if(not self.exists()):
			return True
		log.write("delete host " + str(self.getID()), "debug")
		return self.getDB().deleteById(self.getID())


	def getIDByHostname(self, hostname: str):
		doc = self.getDB().findOne({"hostname": hostname})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def prepareCredential(self):
		cred = self.getCredential()
	
		if(cred):
			self.host_connection.setCredential(cred)		

	def prepare(self):
		exec("from drivers.host_" + self.getType() + " import HostTemplate", globals())
		self.host_connection = HostTemplate(self)
		self.prepareCredential()
	
		if not self.Connect():
			return False
		
		return True

	def getConnection(self):
		return self.host_connection

	def Connect(self):
		try:
			self.getConnection().connect()
		except:
			return False
		finally:
			return True	
