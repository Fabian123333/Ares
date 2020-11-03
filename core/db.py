import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import json

from config import mongodb as conf

client = MongoClient(conf["connection_string"])

dbname="ares"
db = client[dbname]


def parseOutput(out):
	if "_id" in out:
		out["id"] = str(out["_id"])
		del out["_id"]
	
	if(type(out) == dict):
		for k, v in out.items():
			if "_id" in v:
				out[k]["id"] = str(v["_id"])
				del out[k]["_id"]

	if(type(out) == list):
		o = out
		out = []
		
		for j in o:	
			if "_id" in j:
				j["id"] = str(j["_id"])
				del j["_id"]			
			out.append(j)
	
	return json.loads(json_util.dumps(out,default=json_util.default))
	

def getTimestamp():
	now = datetime.datetime.now()
	ts = now.strftime('%Y-%m-%d %H:%M:%S')
	return ts

def exists(id, col_name):
	col = db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def deleteById(id, col_name):
	if(exists(id, col_name)):
		return False
		
	col = db[col_name]
	col.delete_one({ '_id': ObjectId(id) }, limit = 1)
	return True

def getByID(id, col_name):
	if not exists(id, col_name):
		return False
	col = db[col_name]
	ret = col.find_one({ '_id': ObjectId(id) }, limit = 1)
	
	return ret

def setColumn(id, value, col_name):
	col = db[col_name]
	search = { '_id': ObjectId(id) }
	new = { "$set": value }
	col.update_one(search, new)

def getValueByName(id: str, field: str, col_name: str):
	if not exists(id, col_name):
		return False
	col = db[col_name]
	ret = col.find_one({ '_id': ObjectId(id) }, limit = 1)
	
	if field in ret:
		return ret[field]
	return False