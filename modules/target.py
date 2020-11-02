from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import credential, secret

col_name="target"

class StructNew(BaseModel):
	name: str
	fqdn: Optional[str] = None
	description: Optional[str] = None
	ip_address: Optional[str] = None
	location: Optional[str] = ""
	path: Optional[str] = "/ares"
	type: str # support ssh sftp rsync cifs
	credential_id: str

def get(id: str):
	log.write("get target " + id, "debug")
	ret = db.getByID(id, col_name)
	return ret

def prepare(id: str):
	target = get(id)
	exec("from drivers.target_" + target["type"] + " import Target", globals())
	t = Target(target)
	
	if("credential_id" in target):
		cred = credential.get(target["credential_id"])
		if "secret_id" in cred:
			cred["secret"] = secret.getSecret(cred["secret_id"])
		t.setCredential(cred)

def getAll():
	log.write("get all targets", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
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