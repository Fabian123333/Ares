from pymongo import MongoClient

client = MongoClient('mongodb://db:27017/')

dbname="ares"
db = client[dbname]