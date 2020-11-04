import json

from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core.db import DB
from core import log

from modules.credential import Credential

col_name="host"

class Host():
	col_name = "host"

	class StructNew(BaseModel):
		hostname: str
		description: Optional[str] = None
		ip_address: Optional[str] = None
		type: Optional[str] = "linux" # support linux windows 
		credential_id: str

	def __init__(self):
		pass

	def getCredentialID(self):
		if(hasattr(self, credential_id)):
			return self.credential_id
		return False

	def getCredential():
		id = self.getCredentialID()
		if id:
			return credential(self.getCredentialID())
		return False

	def getDB(self):
		return DB(self.col_name)

	def __init__(self, id=None, name=None, data=None):
		if data == None:
			if(name != None and id == None):
				id = self.getIdByName()
			if(id != None and id != False):
				return self.get(id)
		else:
			if id == None:
				return self.create(data)

	def toJSON(self):	
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getIdByName(self, id: str):
		doc = self.getDB().findOne({"name": name})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def create(self, data):
		log.write("create host: " + str(data), "debug")
	
		if(Host(name=data.name).exists()):
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
		return self.exist

	def getName(self):
		if hasattr(self, "name"):
			return self.name
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

	def getIDByHostname(self, hostname: str):
		doc = self.getDB().findOne({"hostname": hostname})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def prepare(self):
		exec("from drivers.host_" + host["type"] + " import HostTemplate", globals())
		h = HostTemplate(host)
	
		cred = sel.fgetCredential()
	
		if(cred):
			h.setCredential(cred)
		h.connect()
		return h
