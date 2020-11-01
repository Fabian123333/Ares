from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import credential, target, host

col_name="target"

class StructJobNew(BaseModel):
	name: str
	description: Optional[str] = None
	type: Optional[str] = "backup"
	snapshots: Optional[int] = 14
	interval: Optional[str] = "12h"
	target_id: int 
	hosts_id: {}

def getAll():
	log.write("get all jobs", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		print(x)
		ret.append(x)

	return ret

def getByName(name: str):
	log.write("get job by name: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"name": name})
	
	for d in doc:
		log.write("found job by name: " + str(doc), "debug")
		return d

	log.write("found no job by name: " + name, "debug")
	return False

def exists(id: str):
	log.write("check if job exists: " + id, "debug")
	col = db.db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def create(data: StructJobNew):
	log.write("create job: " + str(data), "debug")
	col = db.db[col_name]
	
	if(getByName(data.name)):
		log.write("error job already exists: " + str(data), "debug")
		return False
	
	for id in data.hosts_id:
		if not host.exists(id):
			log.write("error host does not exist: " + str(id), "debug")
	
	if not target.exists(data.target_id):
		log.write("error target does not exist: " + str(data.target_id), "debug")
	
	log.write("create target setup: " + str(data))
	
	# doc = {"name": data.name, "description": data.description, "type": target.type, "snapshots": target.ip_address, "type": target.type, "credential_id": target.credential_id}
	doc = data
	x = col.insert_one(doc)
	
	return True