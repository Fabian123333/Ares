from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core.db import DB
from core import log

from modules.secret import Secret

class Credential():
	col_name="credential"
	exist = False

	class StructNew(BaseModel):
		name: str
		type: Optional[str] = "password" # support certificate, token, none and password
		username: Optional[str] = "root"
		description: Optional[str] = None
		secret_id: str
	
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
		r = self
		if hasattr(r, "secret"):
			r.secret = "<hidden>"
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getIdByName(self, id: str):
		doc = self.getDB().findOne({"name": name})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def create(self, data):
		if(Secret(name=data.name)):
			log.write("error creating credential, already exists: " + str(data.name))
			return False
		
		if(not Secret(data.secret_id)):
			log.write("error creating credential, secret not found: " + str(data.secret_id))
			return False
	
		log.write("create credential: " + str(data))
	
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

	def getUsername(self):
		if hasattr(self, "username"):
			return self.username
		return False

	def getType(self):
		if hasattr(self, "type"):
			return self.type
		return False

	def get(self, id: str):
		log.write("load credential by id: " + id, "debug")
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
		log.write("get all credentials", "debug")
		docs = self.getDB().getCollection(query=filter)
		
		if(type == "JSON"):
			return docs
		else:
			ret = []
			for d in docs:
				r = Secret(str(d["_id"]))
				ret.append(r)
			return ret

	def getSecret(self):
		return Secret(self.secret_id).getSecret()