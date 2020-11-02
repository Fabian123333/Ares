import datetime
import uuid
import time

from pydantic import BaseModel
from typing import Optional
from bson.objectid import ObjectId

from core import db
from core import log

from modules import credential, target, host

col_name="job"
lock_interval = 1 # 1min
lock_wait_time = 1 # seconds to wait to ensure integrity

class StructJobNew(BaseModel):
	name: str
	description: Optional[str] = None
	type: Optional[str] = "backup"
	snapshots: Optional[int] = 14
	interval: Optional[int] = 720 # interval in minutes
	target_id: str 
	host_ids: list
	task_ids: list

# get single job
def get(id: str):
	log.write("get job " + id, "debug")
	ret = db.getByID(id, col_name)
	return ret

def start(id):
	db.setColumn(id, {"status":"started"}, col_name)
	return True

def getAll():
	log.write("get all jobs", "debug")
	col = db.db[col_name]
	ret = []
	
	for x in col.find():
		ret.append(x)

	return ret

def getByName(name: str):
	log.write("get job by name: " + name, "debug")
	col = db.db[col_name]
	doc = col.find({"name": name})
	
	for d in doc:
		log.write("found job by name: " + str(doc), "debug")
		return d

	log.write("found no job by name: " + name, "debug")
	return False

def getWorker(id: str):
	if(not col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return False
	db.getValueByName(id, "worker", col_name)


def exists(id: str):
	log.write("check if job exists: " + id, "debug")
	col = db.db[col_name]
	
	if(col.count_documents({ '_id': ObjectId(id) }, limit = 1)):
		return True
	else:
		return False

def create(data: StructJobNew):
	log.write("create job: " + str(data), "debug")
	col = db.db[col_name]
	
	if(getByName(data.name)):
		log.write("error job already exists: " + str(data), "debug")
		return False

	if not target.exists(data.target_id):
		log.write("error target does not exist: " + str(data.target_id), "debug")
	
	log.write("create target setup: " + str(data))

	doc = data.dict()
	x = col.insert_one(doc)
	
	return True

def isLocked(job_id):
	j = get(job_id)
	
	if "lock_time" in j and not "worker" in j:
		lock_expire = datetime.strptime(j.lock_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=lock_interval)
	
		if datetime.datetime.now() > lock_expire:
			return True
	return False


def apply(job_id):
	log.write("apply for job " + job_id, "debug")
	if(not exists(job_id)):
		return False

	if(isLocked(job_id)):
		return False

	log.write("start locking " + job_id, "debug")

	worker=str(uuid.uuid1())

	if(lock(job_id, worker)):
		time.sleep(lock_wait_time)
		if(getValueByName(job_id, "worker") == worker):
			log.write("successfully assigned " + job_id + " to " + worker, "debug")
			return worker

	return False

def getValueByName(job_id, worker):
	return db.getValueByName(job_id, worker, col_name)

def lock(job_id, worker):
	now = datetime.datetime.now()
	lock_time = now.strftime('%Y-%m-%d %H:%M:%S')
	db.setColumn(job_id, {"lock_time":lock_time,"worker":worker}, col_name)
	return True

def delete(job_id):
	log.write("delete job " + job_id, "debug")
	return db.deleteById(job_id, col)

def request():
	log.write("check available job", "debug")
	jobs = getAll()
	
	
	for j in jobs:
		if "last_run" in j:
			next_run = datetime.strptime(j.last_run, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=j.interval)
			if datetime.now() > next_run:
				log.write("found available job", "debug")
				return j
		else:
			log.write("found available job", "debug")
			return j

	return False