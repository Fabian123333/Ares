from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient('mongodb://db:27017/')

dbname="ares"
db = client[dbname]

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