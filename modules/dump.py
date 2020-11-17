import json
import time 

from core.db import DB
from core import log

from modules.job import Job
from modules.task import Task
from modules.target import Target
from modules.host import Host

import os
import datetime

class Dump():
	col_name = "dump"
	
	cmd = { 
			"mongodb" : {
				"dump" : "mongodump -o /dumps",
				"cred_format" : "--uri='%s'",
				"db_format" : "--db="
			},
			"mysql" : {
				"dump": "mysqldump --comments --routines ",
				"dump_all": 'mkdir /dumps; cd /dumps; mysql -N -e "show databases" | grep -vE "^(mysql|performance_schema|information_schema)$" | while read dbname; do mysqldump --complete-insert --routines --triggers --single-transaction "$dbname" > "$dbname".sql; done',
				"db_format" : "%s"
			}
		}		

	def __init__(self, id=None, job=None, source=None, target=None):
		self.filename = ""
		
		log.clearBuffer()
		
		if(job != None):
			self.setJob(job)
		if(source != None):
			self.setSource(source)
		if(target != None):
			self.setTarget(target)
		
		self.start_time = self.getTimestamp()

		if(id != None):
			self.get(id)

	def get(self, id):
		log.write("load dump by id: " + id, "debug")
		ret = self.getDB().get(id)
		
		if ret:
			for k, v in ret.items():
				setattr(self, k, v)
			self.id = str(ret["_id"])
			del(self._id)
			self.exist = True
		else: 
			return False

	def getAll(self, filter={}, type="object"):
		log.write("get all dumps", "debug")
		docs = self.getDB().getCollection(query=filter)
		
		if(type == "JSON"):
			return docs
		else:
			ret = []
			for d in docs:
				r = Dump(str(d["_id"]))
				ret.append(r)
			return ret

	def getCmd(self):
		type = self.task.getType()
		if type:
			return self.cmd[type]
		return False

	def getTimestamp(self):
		now = datetime.datetime.now()
		ts = now.strftime('%Y-%m-%d_%H-%M-%S')
		return ts

	def getDB(self):
		return DB(self.col_name)
	def exists(self):
		if hasattr(self, "exist"):
			return self.exist
		else:
			return False

	def getFilename(self):
		if hasattr(self, "filename"):
			return self.filename
		return False
	
	def getSnapshots(self):
		log.write("get snapshots")
		
		filter = {
			"task_id": self.getTask().getID(),
			"host_id": self.getHost().getID(),
			"target_id": self.getTarget().getID()
		}
		
		ret = self.getDB.find(filter=filter).sort("start_time", 1)
		
		log.write("found %i snapshots" % (ret.count()))
		
		return ret

	def deleteOldestSnapshot(self):
		id = self.getSnapshots()[0]["_id"]
		return Dump(id).delete()

	def purgeOld(self):
		log.write("purge old dumps", "info")
		while self.getSnapshots().count() > self.getJob().getMaxSnapshotCount():
			self.deleteOldestSnapshot()

		return True

	def toJSON(self):	
		r = self
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def getID(self):
		if hasattr(self, "id"):
			return self.id
		else:
			return False

	def setJob(self, job):
		self.job = job

	def getJob(self):
		if not hasattr(self, "job"):
			self.job = Job(self.job)
		return self.job

	def setTarget(self, target):
		self.target = target

	def getTarget(self):
		if not hasattr(self, "target"):
			self.target = Target(self.target_id)
		return self.target
	
	def setSource(self, source):
		self.source = source

	def getSource(self):
		if not hasattr(self, "source"):
			self.source = Host(self.host_id)
		return self.source
	def getTarget(self):
		if not hasattr(self, "target"):
			self.target = Target(self.target_id)
		return self.target

	def getHost(self):
		if not hasattr(self, "host"):
			self.host = Target(self.host_id)
		return self.target
		return ts

	def getType(self):
		if not hasattr(self, "type"):
			return self.type
		return False

	def getTask(self):
		if hasattr(self, "task"):
			return self.task
		return False

	def prepare(self, task):
		self.task = task

	def delete(self):
		if(not self.exists()):
			return True
		log.write("delete dump " + str(self.getID()), "debug")
		
		self.getTarget().prepare()
		self.getTarget().getConnection().deleteFile(self.getFilename())
		return self.getDB().deleteById(self.getID())

	def run(self, task):
		self.task = task
	
		log.write("run task: " + str(self.task.getID()))
		self.prepare(task)

		if self.task.getData("container"):
			for container in self.task.getData("container"):
				self.c = self.task.getData("container")[container]
				log.write("fetch ids for container name: " + container, "debug")
				c_ids = self.source.getContainersByName(container)
				if len(c_ids) == 0:
					log.write("no matching containers found", "debug")
				else:
					for c_id in c_ids:
						self.container_id = c_id
						if "db" in self.c:
							if type(self.c["db"]) is str:
								self.c["db"]= [self.c["db"]]
							
							for db in self.c["db"]:
								self.container = container
								self.filename = self.getDumpFilename(db=db, container=self.container)
								self.backupDB(db=db, container_id=c_id)
	
						else:
							self.container = container
							self.filename = self.getDumpFilename(container=self.container)
							self.backupDB(container_id=c_id)
							
		if self.task.getData("stacks"):
			for stack in self.task.getData("stacks"):			
				self.c = self.task.getData("stacks")[stack]
				log.write("fetch containers for stack name: " + stack, "debug")
				c_ids = self.source.getContainersByStack(stack)
				if len(c_ids) == 0:
					log.write("no matching containers found", "debug")
				else:
					for c_id in c_ids:
						if "db" in self.c:
							if type(self.c["db"]) is str:
								self.c["db"] = [self.c["db"]]
							
							for db in self.c["db"]:
								self.filename = self.getDumpFilename(db=db, stack=stack)
								self.backupDB(db=db, container_id=c_id)
						
						else:
							self.filename = self.getDumpFilename(stack=stack)
							self.backupDB(container_id=c_id)

	def getDumpFilename(self, db=None, container=None, stack=None):
		base = "/dumps/" + str(self.job.getID()) + "/" + self.task.getID() + "/"

		if(stack != None):
			base += stack + "/"
		if(container != None):
			base += container + "/"
		
		if(db != None):
			filename = self.getTimestamp() + "_" + db
		else:
			filename = self.getTimestamp()
		
		if self.task.getType() == "mongodb":
			filename += ".tar"
		elif self.task.getType() == "mysql":
			filename += ".tar"
		
		return base + filename

	def getFilename(self):
		if hasattr(self, "filename"):
			return self.filename
		return False

	def backupDB(self, db=None, container_id=None):
		state = False
		backup_root = os.path.dirname(self.getFilename())
		if(not self.target.fileExists(backup_root)):
			log.write("dump root does not exist. creating: " + backup_root)
			self.target.createDirectoryRecursive(backup_root)

		cmd = self.getCmd()["dump"]

		if "port" in self.c:
			cmd += " --port " + str(self.c["port"])

		if(db != None):
			cmd += " " + self.getCmd()["db_format"] + db 
		elif("dump_all" in self.getCmd()):
			cmd = self.getCmd()["dump_all"]

		if "gzip" in self.c:
			cmd += " | gzip"

		self.target.openFile(self.filename)
		
		if(container_id != None):
			self.source.execCommandDocker(container_id, cmd)
		else:
			self.source.execCommand(cmd)

		if(self.task.getType() in ["mongodb", "mysql"]):
			data = self.source.read()
		
			if(container_id != None):
				self.source.execCommandDocker(container_id, "tar -Oc /dumps 2>/dev/null | cat", wait=False)
			else:
				self.source.execCommand("tar -Oc /dumps 2>/dev/null | cat")

		while True:
			data = self.source.readBinary()
			state = True
			if not data:
				break
			self.target.writeFile(data)
		
		if(self.task.getType() in ["mongodb", "mysql"]):
			if(container_id != None):
				self.source.execCommandDocker(container_id, "rm -rf /dumps")
			else:
				self.source.execCommand("rm -rf /dumps")
		self.target.closeFile()
		
		if(state == False):
			log.write("error: no data received", "error")
			self.getTarget().getConnection().deleteFile()
		else:
			self.addDumpEntry()
			log.write("finish dump")

	def addDumpEntry(self, data={}):
		log.write("mark dump as compeleted", "debug")
		
		self.end_time = self.getTimestamp()
		
		doc = {"job_id": str(self.job.getID()), 
				"filename": self.filename, 
				"task_id": self.task.getID(), 
				"host_id": self.source.conf.getID(), 
				"target_id": self.target.conf.getID(),
				"type": self.task.getType(),
				"hostname": self.source.conf.getHostname(), "log": log.getBuffer(),"start_time": self.start_time, "end_time": self.end_time}
		
		self.getDB().addDoc(doc)