from core import log, db

import os
import datetime

col_name = "backup"

class Backup():
	def __init__(self, job, source, target):
		log.clearBuffer()
		self.start_time = self.getTimestamp()
		self.job = job
		self.source = source
		self.target = target
		self.filename = ""

	def getTimestamp(self):
		now = datetime.datetime.now()
		ts = now.strftime('%Y-%m-%d_%H-%M-%S')
		return ts

	def getNewBackupPath(self):
		return self.getBackupRoot() + "/" + self.start_time + "-" + self.task["name"] + ".tar.gz"

	def getContainerBackupPath(self, name):
		return self.getBackupRoot() + "/" + self.start_time + "-" + name + ".tar.gz"

	def getStackBackupPath(self, stack, name):
		return self.getBackupRootShort() + "/" + stack + "/" + self.start_time + "-" + name + ".tar.gz"


	def run(self, task):
		self.task = task
	
		log.write("run task: " + str(task["_id"]))
		self.prepare(task)

		if(task["type"] == "file"):
			log.write("init file backup", "notice")
			self.filename = self.getNewBackupPath()
			
			self.backupFile()
			
			return True

		elif(task["type"] == "docker"):
			log.write("init docker backup", "notice")
			c_ids = []
			
			if "container" in task["data"]:
				for container in task["data"]["container"]:
					log.write("fetch ids for container name: " + container, "debug")
					c_ids = self.source.getContainersByName(container)		
					if len(c_ids) == 0:
						log.write("no matching containers found", "debug")
					else:
						for id in c_ids:
							self.filename = self.getContainerBackupPath(container)
							self.backupDockerContainer(id, container)

			if "stacks" in task["data"]:
				for stack in task["data"]["stacks"]:			
					log.write("fetch containers for stack name: " + stack, "debug")
					c_names = self.source.getContainersByStack(stack)
					if len(c_names) == 0:
						log.write("no matching containers found", "debug")
					else:
						for container in c_names:
							filename = self.getStackBackupPath(stack, container)
							for id in self.source.getContainersByName(container):
								self.backupDockerContainer(id, container, stack)

			# self.target.openFile(filename)
		else:
			log.write("error unsupported task type: " + task["type"])

	def backupFile(self):
		if(not self.target.fileExists(self.getBackupRoot())):
			log.write("backup root does not exist. creating: " + self.getBackupRoot())
			self.target.createDirectoryRecursive(self.getBackupRoot())
			
		self.target.openFile(self.filename)
		self.source.createArchiveFromPaths(self.task["data"])
						
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

		if not self.target.fileExists(os.path.dirname(filename)):
			log.write("backup root does not exist. creating: " + os.path.dirname(filename))
			self.target.createDirectoryRecursive(os.path.dirname(filename))
		
		self.target.openFile(filename)
		self.source.createArchiveFromContainerId(id)
					
		while True:
			data = self.source.readBinary()
			if not data:
				break
			self.target.writeFile(data)
		
		self.target.closeFile()

		log.write("finish backup of container %s" % (id))
		
		log = {"container": container}
		if not stack == None:
			log += {"stack": stack}
		
		self.addBackupEntry(log)
		return True		

	def addBackupEntry(self, data={}):
		log.write("mark backup as compeleted", "debug")
		
		self.end_time = self.getTimestamp()
		
		doc = {"job_id": str(self.job["_id"]), 
				"file": self.filename, 
				"task_id": str(self.task["_id"]), 
				"host_id": self.source.id, 
				"type": self.task["type"],
				"hostname": self.source.hostname, "log": log.getBuffer(),"start_time": self.start_time, "end_time": self.end_time}
		
		db.addDoc(doc, col_name)
	
	def getBackupRootShort(self):
		return "/backup/" + str(self.job["_id"]) + "/" + str(self.task["_id"]) + "/"
	
	def getBackupRootStack(self, stack):
		return "/backup/" + str(self.job["_id"]) + "/" + str(self.task["_id"]) + "/" + stack + "/"
	
	def getBackupRoot(self):
		return "/backup/" + str(self.job["_id"]) + "/" + str(self.task["_id"]) + "/" + self.source.host + "/"

	def prepare(self, task):
		self.task = task