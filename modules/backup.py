import json

from core.db import DB
from core import log

from modules.job import Job
from modules.task import Task
from modules.target import Target
from modules.host import Host

import os
import datetime

class Backup():
	col_name = "backup"
	
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

	def getID(self):
		if hasattr(self, "id"):
			return self.id
		else:
			return False

	def getAll(self, filter={}, type="object"):
		log.write("get all backups", "debug")
		docs = self.getDB().getCollection(query=filter)
		
		if(type == "JSON"):
			return docs
		else:
			ret = []
			for d in docs:
				r = Backup(str(d["_id"]))
				ret.append(r)
			return ret

	def getTarget(self):
		if not hasattr(self, "target"):
			self.target = Target(self.target_id)
		return self.target

	def getHost(self):
		if not hasattr(self, "host"):
			self.host = Target(self.host_id)
		return self.target

	def get(self, id):
		log.write("load backup by id: " + id, "debug")
		ret = self.getDB().get(id)
		
		if ret:
			for k, v in ret.items():
				setattr(self, k, v)
			self.id = str(ret["_id"])
			del(self._id)
			self.exist = True
		else: 
			return False

	def getDB(self):
		return DB(self.col_name)

	def toJSON(self):	
		r = self
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

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

	def getTimestamp(self):
		now = datetime.datetime.now()
		ts = now.strftime('%Y-%m-%d_%H-%M-%S')
		return ts

	def getNewBackupPath(self):
		return self.getBackupRoot() + "/" + self.start_time + "-" + self.task.getName() + ".tar.gz"

	def getContainerBackupPath(self, name):
		return self.getBackupRoot() + "/" + self.start_time + "-" + name + ".tar.gz"

	def getStackBackupPath(self, stack, name):
		return self.getBackupRootShort() + "/" + stack + "/" + self.start_time + "-" + name + ".tar.gz"

	def run(self, task):
		self.task = task
	
		log.write("run task: " + str(self.task.getID()))
		self.prepare(task)

		if(self.task.getType() == "file"):
			log.write("init file backup", "notice")
			self.filename = self.getNewBackupPath()
			
			self.backupFile()
			
			return True

		elif(self.task.getType() == "docker"):
			log.write("init docker backup", "notice")
			c_ids = []
			
			if self.task.getData("container"):
				for container in self.task.getData("container"):
					log.write("fetch ids for container name: " + container, "debug")
					c_ids = self.source.getContainersByName(container)		
					if len(c_ids) == 0:
						log.write("no matching containers found", "debug")
					else:
						for id in c_ids:
							self.filename = self.getContainerBackupPath(container)
							self.backupDockerContainer(id, container)

			if self.task.getData("stacks"):
				for stack in self.task.getData("stacks"):			
					log.write("fetch containers for stack name: " + stack, "debug")
					c_names = self.source.getContainersByStack(stack)
					if len(c_names) == 0:
						log.write("no matching containers found", "debug")
					else:
						for container in c_names:
							self.filename = self.getStackBackupPath(stack, container)
							for id in self.source.getContainersByName(container):
								self.backupDockerContainer(id, container, stack)

			self.purgeOld()
			log.write("finish docker backup", "debug")

			# self.target.openFile(filename)
		else:
			log.write("error unsupported task type: " + task["type"])

	def backupFile(self):
		if(not self.target.fileExists(self.getBackupRoot())):
			log.write("backup root does not exist. creating: " + self.getBackupRoot())
			self.target.createDirectoryRecursive(self.getBackupRoot())
			
		self.target.openFile(self.filename)
		self.source.createArchiveFromPaths(self.task.getData())
						
		while True:
			data = self.source.readBinary()
			if not data:
				break
			self.target.writeFile(data)
			
		log.write("finish backup")

		self.addBackupEntry()
		self.target.closeFile()


	def backupDockerContainer(self, id, container, stack=None):
		log.write("start backup of container %s to %s" % (id, self.filename))

		if not self.target.fileExists(os.path.dirname(self.getFilename())):
			log.write("backup root does not exist. creating: " + os.path.dirname(self.getFilename()))
			self.target.createDirectoryRecursive(os.path.dirname(self.getFilename()))

		self.target.openFile(self.getFilename())
		self.source.createArchiveFromContainerId(id)
					
		while True:
			data = self.source.readBinary()
			if not data:
				break
			self.target.writeFile(data)
		
		self.target.closeFile()

		log.write("finish backup of container %s" % (id))
		
		logs = {"container": container}
		if not stack == None:
			logs["stack"] = stack
		
		self.addBackupEntry(logs)
		return True		

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
		return Backup(id).delete()

	def purgeOld(self):
		log.write("purge old backups", "info")
		while self.getSnapshots().count() > self.getJob().getMaxSnapshotCount():
			self.deleteOldestSnapshot()

		return True

	def addBackupEntry(self, data={}):
		log.write("mark backup as compeleted", "debug")
		
		self.end_time = self.getTimestamp()
		
		doc = {"job_id": str(self.job.getID()), 
				"filename": self.filename, 
				"task_id": self.task.getID(), 
				"host_id": self.source.conf.getID(), 
				"target_id": self.target.conf.getID(),
				"type": self.task.getType(),
				"hostname": self.source.conf.getHostname(), "log": log.getBuffer(),"start_time": self.start_time, "end_time": self.end_time}
		
		self.getDB().addDoc(doc)

	def restore(self, overwrite=True, replace=False):
		if(self.task.getType() == "file"):
			log.write("restore backup " + self.getID(), "notice")
			self.getTarget().prepare()
			self.getTarget().getConnection().openFile(self.getFilename(), "rb")
	
			self.getSource().prepare()
			self.getSource().getConnection().restoreArchive()
	
			while True:
				data = self.getTarget().getConnection().readBinary()
				if not data:
					break
				self.getSource().getConnection().writeBinary(data)
			self.getSource().getConnection().closeFile()
			self.getSource().getConnection().syncDirectory()
			
			log.write("restored backup " + self.getID())
		else:
			log.write("error: restore not supported for this type", "error")
			return False

	def getBackupRootShort(self):
		return "/backup/" + str(self.job.getID()) + "/" + self.task.getID() + "/"
	
	def getBackupRootStack(self, stack):
		return "/backup/" + str(self.job.getID()) + "/" + self.task.getID() + "/" + stack + "/"
	
	def getBackupRoot(self):
		return "/backup/" + str(self.job.getID()) + "/" + self.task.getID() + "/" + self.source.conf.getHostname() + "/"

	def getTask(self):
		if hasattr(self, "task"):
			return self.task
		return False

	def prepare(self, task):
		self.task = task

	def delete(self):
		if(not self.exists()):
			return True
		log.write("delete backup " + str(self.getID()), "debug")
		
		self.getTarget().prepare()
		self.getTarget().getConnection().deleteFile(self.getFilename())
		return self.getDB().deleteById(self.getID())