import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import json

from config import mongodb as conf

client = MongoClient(conf["url"])

dbname="ares"
db = client[dbname]

class DB():
	db = "ares"
	url = "mongodb://db:27017/"
	col = ""
	
	def __init__(self, col_name):
		self.col = col_name
		
		self.loadConfig()
		self.connect()
	
	def loadConfig(self):
		for k, v in conf.items():
			setattr(self, k, v)
	
	def getConnectionString(self):
		return self.url
	
	def connect(self):
		self.client = MongoClient(self.getConnectionString())
		self.db = self.client[self.db]
		self.col = self.db[self.col]

	def getCollection(self, query={}):
		ret = []
		
		for x in self.col.find(query):
			ret.append(x)
		return ret

	def updateDocByID(self, id, value):
		search = { '_id': ObjectId(id) }
		new = { "$set": value }
		return self.col.update_one(search, new)

	def getTimestamp():
		now = datetime.datetime.now()
		ts = now.strftime('%Y-%m-%d %H:%M:%S')
		return ts

	def addDoc(self, doc):
		x = self.col.insert_one(doc)
		if x:
			return True
		else:
			return False

	def deleteById(self, id):
		if(not self.exists(id)):
			return False
			
		return self.col.delete_one({ '_id': ObjectId(id) }, limit = 1)

	def get(self, id):
		if not self.exists(id):
			return False
		ret = self.col.find_one({ '_id': ObjectId(id) }, limit = 1)
		
		return ret	

	def exists(self, id):
		if(self.col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
			return True
		else:
			return False

	def findOne(pattern):
		return self.col.find_one(pattern)
