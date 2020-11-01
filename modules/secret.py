from pydantic import BaseModel
from typing import Optional

from bson.objectid import ObjectId

from core import db
from core import log

from modules import credential

col_name="secret"

class Secret(BaseModel):
	id: int = 0
	name: str
	description: Optional[str] = None
	secret: str

class StructNew(BaseModel):
	name: str
	description: Optional[str] = None
	secret: str

def getAll():
	log.write("getAllSecrets", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		print(x)
		ret.append(x)

	return ret

def exists(id: str):
	log.write("check if secret exists: " + id, "debug")
	col = db.db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def getByName(name: str):
	log.write("getSecretByName: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"name": name})
	
	for d in doc:
		log.write("getSecretByName found: " + str(doc), "debug")
		return d

	log.write("getSecretByName not found: " + name, "debug")
	return False

def create(secret: StructNew):
	log.write("createSecret: " + str(secret), "debug")
	col = db.db[col_name]
	
	if(getByName(secret.name)):
		return False
	
	log.write("createSecret setup: " + str(secret))
	
	doc = {"name": secret.name, "description": secret.description, "secret": secret.secret}
	x = col.insert_one(doc)
	
	return True
