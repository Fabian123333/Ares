from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import credential

col_name="target"

class StructNew(BaseModel):
	name: str
	fqdn: Optional[str] = None
	description: Optional[str] = None
	ip_address: Optional[str] = None
	type: str # support ssh sftp rsync cifs
	credential_id: str


def getAll():
	log.write("get all targets", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		print(x)
		ret.append(x)

	return ret

def getByName(name: str):
	log.write("get target by name: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"name": name})
	
	for d in doc:
		log.write("found target by name: " + str(doc), "debug")
		return d

	log.write("found no target by name: " + name, "debug")
	return False

def exists(id: str):
	log.write("check if target exists: " + id, "debug")
	col = db.db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def create(target: StructNew):
	log.write("create target: " + str(target), "debug")
	col = db.db[col_name]
	
	if(getByName(target.name)):
		log.write("error target already exists: " + str(target), "debug")
		return False
	
	if(not credential.exists(target.credential_id)):
		log.write("error target does not exist: " + str(target.credential_id), "debug")	
		return False
	
	log.write("create target setup: " + str(target))
	
	doc = {"name": target.name, "description": target.description, "fqdn": target.fqdn, "ip_address": target.ip_address, "type": target.type, "credential_id": target.credential_id}
	x = col.insert_one(doc)
	
	return True