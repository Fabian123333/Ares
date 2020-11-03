from core import log, db
import datetime

col_name = "backup"

class Backup():
	def __init__(self, job, source, target):
		log.clearBuffer()
		self.start_time = self.getTimestamp()
		self.job = job
		self.source = source
		self.target = target

	def getTimestamp(self):
		now = datetime.datetime.now()
		ts = now.strftime('%Y-%m-%d_%H-%M-%S')
		return ts

	def getNewBackupPath(self):
		#return self.getBackupRoot() + "/" + self.start_time + "-ares.tar.gz"
		return self.getBackupRoot() + "/" + self.start_time + "-" + self.task["name"] + ".tar.gz"

	def run(self, task):
		self.task = task
		filename = self.getNewBackupPath()
	
		log.write("run task: " + str(task["_id"]))
		self.prepare(task)
		if(task["type"] == "file"):
			archiv = ""
			data = True

			self.target.openFile(filename)
			self.source.createArchiveFromPaths(task["data"])
						
			while True:
				data = self.source.readBinary()
				if not data:
					break
				self.target.writeFile(data)
			
			log.write("finish backup")
			
			self.target.closeFile()
			self.complete()
			
			return True
		else:
			log.write("error unsupported task type: " + task["type"])

	def complete(self):
		log.write("mark backup as compeleted", "debug")
		col = db.db[col_name]
		
		self.end_time = self.getTimestamp()
		
		doc = {"job_id": str(self.job["_id"]), "task_id": str(self.task["_id"]), "host_id": self.source.id, "hostname": self.source.hostname, "log": log.getBuffer(),"start_time": self.start_time, "end_time": self.end_time}
		x = col.insert_one(doc)
		return True
		
	def getBackupRoot(self):
		return "/backup/" + str(self.job["_id"]) + "/" + str(self.task["_id"]) + "/" + self.source.host

	def prepare(self, task):
		self.task = task
		if(not self.target.fileExists(self.getBackupRoot())):
			log.write("backup root does not exist. creating: " + self.getBackupRoot())
			self.target.createDirectoryRecursive(self.getBackupRoot())