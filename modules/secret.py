import json

from bson.objectid import ObjectId

from core.db import DB
from core import log

class Secret():
	exist = False

	col_name = "secret"

	def getDB(self):
		return DB(self.col_name)

	def __init__(self, id=None, name=None, data=None):

		if data == None:
			if(name != None and id == None):
				id = self.getIdByName()
			if(id != None and id != False):
				self.get(id)
		else:
			if id == None:
				self.create(data)

	def toJSON(self):	
		r = self
		if hasattr(r, "secret"):
			r.secret = "<hidden>"
		return json.dumps(r, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getIdByName(self, id: str):
		doc = self.getDB().findOne({"name": name})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def create(self, data):
		log.write("create secret: " + str(data), "debug")
	
		if(Secret(name=data.name).exists()):
			log.write("error secret already exists: " + str(data), "debug")
			return False

		log.write("create secret: " + str(data))
	
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

	def getName(self):
		if hasattr(self, "name"):
			return self.name
		return False

	def get(self, id: str):
		log.write("load secret by id: " + id, "debug")
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
		log.write("get all secrets", "debug")
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
		log.write("get secret: " + self.id, "debug")
		return self.secret

	def update(self, data):
		if not self.exists():
			return False
		
		value = dict()
		for k, v in vars(data).items():
			if v != None:
				value[k] = v

		log.write("update secret %s (%s)" % (self.getID(), value))
		update = self.getDB().updateDocByID(self.id, value)
		self.get(self.getID())
		return True

	def delete(self):
		if(not self.exists()):
			return True
		log.write("delete secret " + str(self.getID()), "debug")
		return self.getDB().deleteById(self.getID())
