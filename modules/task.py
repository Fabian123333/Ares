from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import credential

col_name="task"

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

def get(id: str):
	log.write("get task " + id, "debug")
	ret = db.getByID(id, col_name)
	return ret

def getAll():
	log.write("get all tasks", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		print(x)
		ret.append(x)

	return ret

def getByName(name: str):
	log.write("get task by name: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"name": name})
	
	for d in doc:
		log.write("found task by name: " + str(doc), "debug")
		return d

	log.write("found no task by name: " + name, "debug")
	return False

def exists(id: str):
	log.write("check if task exists: " + id, "debug")
	col = db.db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def create(data: StructTaskNew):
	log.write("create task: " + str(data), "debug")
	col = db.db[col_name]
	
	if(getByName(data.name)):
		log.write("error task already exists: " + str(data), "debug")
		return False

	log.write("create task: " + str(data))
	
	doc = data.dict()
	x = col.insert_one(doc)
	
	return True