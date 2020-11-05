import json

from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core import log

from core.db import DB

from modules import credential

class Task():
	col_name = "task"
	exist = False
	name: str

	class StructTaskFilter(BaseModel):
		filter: Optional[dict] # support file, database, partition

		class Config:
			schema_extra = {
				"example": {
					"filter": {
						"name": "Docker Backup",
						"type": "file"
					}
				}
			}		
		

	class StructTaskNew(BaseModel):
		name: str
		type: Optional[str] = "file" # support file, database, partition
		description: Optional[str] = None
		data: dict
		
		class Config:
			schema_extra = {
				"example": {
					"name": "Docker Backup",
					"type": "file",
					"data": {
						"container": ["dyndns_app"],
						"stacks": ["ares", "fhem", "swarmpit", "unifi"]
					}
				}
			}

	def __init__(self, id=None, name=None, data=None):

		if data == None:
			if(name != None and id == None):
				id = self.getIdByName()
			if(id != None and id != False):
				self.get(id)
		else:
			if id == None:
				self.create(data)

	def getDB(self):
		return DB(self.col_name)
		
	def toJSON(self):	
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getIdByName(self, id: str):
		doc = self.getDB().findOne({"name": name})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def create(self, data):
		log.write("create task: " + str(data), "debug")
	
		if(Task(name=data.name).exists()):
			log.write("error task already exists: " + str(data), "debug")
			return False

		log.write("create task: " + str(data))
	
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
		log.write("load task by id: " + id, "debug")
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
		log.write("get all tasks", "debug")
		docs = self.getDB().getCollection(query=filter)
		
		if(type == "JSON"):
			return docs
		else:
			ret = []
			for d in docs:
				c_task = Task(str(d["_id"]))
				ret.append(c_task)
			return ret

	def getData(self, type=None):
		if hasattr(self, "data"):
			if type == None:
				return self.data
			if hasattr(self.data, type):
				return self.data[type]
		return False
	
	def getType(self):
		if hasattr(self, "type"):
			return self.type
		else:
			return False

	def setType(self, val: str):
		if self.getDB().updateDocByID(self.id, {"type":val}):
			self.type = val
			return True
		else:
			return False
