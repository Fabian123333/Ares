from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import credential

col_name="host"

class StructNew(BaseModel):
	hostname: str
	description: Optional[str] = None
	ip_address: Optional[str] = None
	type: Optional[str] = "linux" # support linux windows 
	credential_id: str


def getAll():
	log.write("get all hosts", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		print(x)
		ret.append(x)

	return ret

def exists(id: str):
	log.write("check if host exists: " + id, "debug")
	col = db.db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def getByHostname(name: str):
	log.write("get host by hostname: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"hostname": name})
	
	for d in doc:
		log.write("found host by hostname: " + str(doc), "debug")
		return d

	log.write("found no host by hostname: " + name, "debug")
	return False

def create(host: StructNew):
	log.write("create host: " + str(host), "debug")
	col = db.db[col_name]
	
	if(getByHostname(host.hostname)):
		log.write("error host already exists: " + str(host), "debug")
		return False
	
	if(not credential.exists(host.credential_id)):
		log.write("error credential does not exist: " + str(host.credential_id), "debug")	
		return False
	
	log.write("create host setup: " + str(host))
	
	doc = {"hostname": host.hostname, "description": host.description, "ip_address": host.ip_address, "type": host.type, "credential_id": host.credential_id}
	x = col.insert_one(doc)
	
	return True