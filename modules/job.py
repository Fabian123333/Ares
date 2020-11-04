import datetime
import uuid
import time
import json

from pydantic import BaseModel
from typing import Optional
from bson.objectid import ObjectId

from core.db import DB
from core import log

from modules import credential, target, host

col_name="job"
lock_interval = 1 # 1min
lock_wait_time = 0 # seconds to wait to ensure integrity

class Job():
	col_name = "job"
	lock_wait_time = 0 # sec to ensure lock
	lock_interval = 1 # 1min
	exist = False

	class StructNew(BaseModel):
		name: str
		description: Optional[str] = None
		type: Optional[str] = "backup"
		snapshots: Optional[int] = 14
		interval: Optional[int] = 720 # interval in minutes
		target_id: str 
		host_ids: list
		task_ids: list

	def getDB(self):
		return DB("job")

	def __init__(self, id=None, name=None, data=None):

		if data == None:
			if(name != None and id == None):
				id = getIdByName()
			if(id != None and id != False):
				return self.get(id)
		else:
			if id == None:
				return self.create(data)

	def toJSON(self):	
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getTarget(self):
		if hasattr(self, "target_id"):
			return self.target_id
		else:
			return False

	def getHosts(self):
		if hasattr(self, "host_ids"):
			return self.host_ids
		else:
			return False
			
	def getTasks(self):
		if hasattr(self, "task_ids"):
			return self.task_ids
		else:
			return False
			
	def getType(self):
		if hasattr(self, "type"):
			return self.type
		else:
			return False

	def setType(self, val: str):
		if self.getDB().updateDocByID(self.id, {"type":val}):
			self.type = val
			return True
		else:
			return False

	def create(self, data):
		log.write("create job: " + str(data), "debug")
	
		if(Job(data["name"])):
			log.write("error job already exists: " + str(data), "debug")
			return False

		if not target.exists(data.target_id):
			log.write("error target does not exist: " + str(data.target_id), "debug")
	
		log.write("create target setup: " + str(data))

		doc = data.dict()
		if self.getDB().addDoc(doc):
			return True
		else:
			return False

	def delete(self):
		log.write("delete job " + self.id, "debug")
		return self.getDB().deleteById(job_id)

	def exists(self):
		return self.exist

	def get(self, id: str):
		log.write("load job by id: " + id, "debug")
		ret = self.getDB().get(id)
		
		if ret:
			for k, v in ret.items():
				setattr(self, k, v)
			self.id = str(ret["_id"])
			del(self._id)
			self.exist = True
		else: 
			return False

	def getIdByName(self, id: str):
		doc = self.getDB().findOne({"name": name})
		
		if not doc:
			return False
	
		return str(doc["_id"])

	def getID(self):
		if hasattr(self, "id"):
			return self.id
		else:
			return False

	def setStatus(self, status: str):
		if self.getDB().updateDocByID(self.id, {"status":status}):
			self.status = status
			return True
		else:
			return False

	def getStatus(self):
		if hasattr(self, "status"):
			return self.status
		else:
			return False

	def setLastRun(self):
		now = DB.getTimestamp()
		self.getDB().updateDocByID(self.id, 
			{"status":"finished", "last_run": now})
		self.last_run = now
		return True

	def getLastRun(self):
		if hasattr(self, "last_run"):
			return self.last_run
		else:
			return False

	def getNextRun(self):
		if hasattr(self, "last_run"):
			return datetime.datetime.strptime(self.getLastRun(), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=self.interval)
		else:
			return datetime.datetime.now()

	def getName(self):
		if hasattr(self, "name"):
			return self.name
		else:
			return False
		
	def getAll(self, type="object"):
		log.write("get all jobs", "debug")
		docs = self.getDB().getCollection()
		
		if(type == "JSON"):
			return docs
		else:
			ret = []
			for d in docs:
				c_job = Job(str(d["_id"]))
				ret.append(c_job)
			return ret

	def getWorker(self):
		if hasattr(self, "worker"):
			return self.worker
		else:
			return False

	def setWorker(self, id: str):
		if self.getDB().updateDocByID(self.id, {"worker":id}):
			self.worker = id
			return True

	def lock(self, worker):
		now = datetime.datetime.now()
		self.lock_time = now.strftime('%Y-%m-%d %H:%M:%S')
		self.getDB().updateDocByID(self.id, {"lock_time":self.lock_time,"worker":worker})
		self.worker = worker
		return True

	def isLocked(self):
		if hasattr(self, "lock_time") and not hasattr(self, "worker"):
			lock_expire = datetime.strptime(self.lock_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=self.lock_interval)
			
			if datetime.datetime.now() > lock_expire:
				return True
		return False

	def apply(self):
		log.write("apply for job " + self.id, "debug")
		if(not self.exists()):
			return False
	
		if(self.isLocked()):
			return False
	
		log.write("start locking " + self.id, "debug")
	
		worker=str(uuid.uuid1())
	
		if(self.lock(worker)):
			time.sleep(self.lock_wait_time)
			if(self.getWorker() == self.worker):
				log.write("successfully assigned " + self.id + " to " + self.worker, "debug")
				return True
		return False

	def request(self):
		jobs = self.getAll()
		for job in jobs:
			if datetime.datetime.now() > job.getNextRun():
				log.write("found available job: " + job.getID(), "debug")
				return job
				
		log.write("found no jobs", "debug")
		return False
