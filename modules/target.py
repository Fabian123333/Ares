import json
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core.db import DB
from core import log

from modules.credential import Credential

col_name="target"


from core import log

from modules.credential import Credential

class Target():
	col_name = "target"

	def __init__(self, id=None, name=None, data=None):
		if data == None:
			if(hostname != None and id == None):
				id = self.getIdByHostname()
			if(id != None and id != False):
				return self.get(id)
		else:
			if id == None:
				return self.create(data)

	def update(self, data):
		if not self.exists():
			return False
		
		value = dict()
		for k, v in vars(data).items():
			if v != None:
				value[k] = v

		log.write("update target %s (%s)" % (self.getID(), value))
		update = self.getDB().updateDocByID(self.id, value)
		self.get(self.getID())
		return True

	def delete(self):
		if(not self.exists()):
			return True
		log.write("delete target " + str(self.getID()), "debug")
		return self.getDB().deleteById(self.getID())

	def getCredentialID(self):
		if(hasattr(self, "credential_id")):
			return self.credential_id
		return False

	def getFQDN(self):
		if(hasattr(self, "fqdn")):
			return self.fqdn
		return False	

	def getCredential(self):
		id = self.getCredentialID()
		if id:
			return Credential(self.getCredentialID())
		return False

	def getDB(self):
		return DB(self.col_name)

	def __init__(self, id=None, name=None, data=None):
		if data == None:
			if(name != None and id == None):
				id = self.getIdByHostname(name)
			if(id != None and id != False):
				self.get(id)
		else:
			if id == None:
				self.create(data)

	def toJSON(self):	
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getIPAdress(self):
		if hasattr(self, "ip_address"):
			return self.ip_address
		return False

	def getType(self):
		if hasattr(self, "type"):
			return self.type
		return Fal

	def getIdByHostname(self, name: str):
		doc = self.getDB().findOne({"hostname": name})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def create(self, data):
		log.write("create target: " + str(data), "debug")
	
		if(Target(name=data.hostname).exists()):
			log.write("error target already exists: " + str(data), "debug")
			return False

		log.write("create target: " + str(data))
	
		doc = data.dict()
		return self.getDB().addDoc(doc)

	def getID(self):
		if hasattr(self, "id"):
			return self.id
		else:
			return False

	def exists(self):
		if hasattr(self, "exist"):
			return self.exist
		else:
			return False

	def getName(self):
		if hasattr(self, "name"):
			return self.name
		return False

	def get(self, id: str):
		log.write("load target by id: " + id, "debug")
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
		log.write("get all targets with filter " + str(filter), "debug")
		docs = self.getDB().getCollection(query=filter)
		
		if(type == "JSON"):
			return docs
		else:
			ret = []
			for d in docs:
				r = Target(str(d["_id"]))
				ret.append(r)
			return ret

	def getIDByHostname(self, hostname: str):
		doc = self.getDB().findOne({"hostname": hostname})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def prepare(self):
		exec("from drivers.target_" + self.getType() + " import TargetTemplate", globals())
		t = TargetTemplate(self)
	
		cred = self.getCredential()
		
		if(cred):
			t.setCredential(cred)
		t.connect()
		
		self.target_connection = t

	def getConnection(self):
		return self.target_connection