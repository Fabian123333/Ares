from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import credential

col_name="host"

class StructHostNew(BaseModel):
	hostname: str
	description: Optional[str] = None
	ip_address: Optional[str] = None
	type: Optional[str] = "linux" # support linux windows 
	credential_id: str

def prepare(id: str):
	host = get(id)
	print(host)
	
	exec("from drivers.host_" + host["type"] + " import Host", globals())
	h = Host(host)
	#t = Target(target)
	#
	#if("credential_id" in target):
	#	cred = credential.get(target["credential_id"])
	#	if "secret_id" in cred:
	#		cred["secret"] = secret.getSecret(cred["secret_id"])
	#	t.setCredential(cred)
	#t.connect()
	#return t

def get(id: str):
	log.write("get host " + id, "debug")
	ret = db.getByID(id, col_name)
	return ret

def getAll():
	log.write("get all hosts", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		ret.append(x)

	return ret

def exists(id: str):
	log.write("check if host exists: " + id, "debug")
	return db.exists(id, col_name)

def getByHostname(name: str):
	log.write("get host by hostname: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"hostname": name})
	
	for d in doc:
		log.write("found host by hostname: " + str(doc), "debug")
		return d

	log.write("found no host by hostname: " + name, "debug")
	return False

def create(host: StructHostNew):
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