from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import secret

col_name="credential"

class StructNew(BaseModel):
	name: str
	type: Optional[str] = "password" # support key, token and password
	username: Optional[str] = "root"
	description: Optional[str] = None
	secret_id: str

def get(id: str):
	log.write("get credential " + id, "debug")
	ret = db.getByID(id, col_name)
	return ret

def getAll():
	get = db.db[col_name]
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		print(x)
		ret.append(x)

	return ret

def getByName(name: str):
	log.write("get credential by name: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"name": name})
	
	for d in doc:
		log.write("found credential by name: " + str(doc), "debug")
		return d

	log.write("found no credential by name: " + name, "debug")
	return False

def exists(id: str):
	log.write("check if credential exists: " + id, "debug")
	col = db.db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def create(credential: StructNew):
	col = db.db[col_name]
	
	if(getByName(credential.name)):
		log.write("error creating credential, already exists: " + str(credential.name))
		return False
	
	if(not secret.exists(credential.secret_id)):
		log.write("error creating credential, secret not found: " + str(credential.secret_id))
		return False

	doc = {"name": credential.name, "type": credential.type, "username": credential.username, "description": credential.description, "secret_id": credential.secret_id}
	x = col.insert_one(doc)
	log.write("create credential: " + str(credential))
	
	return True
