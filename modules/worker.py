from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules.job import Job
from modules.task import Task
from modules.host import Host

from modules.backup import Backup
from modules.dump import Dump

class Worker():
	def __init__(self):
		log.write("init worker", "debug")
		self.uuid:str = None

	def prepareSource(self):
		pass

	def execJob(self, job):
		log.write("exec job " + job.id , "notice")
		job.setStatus("started")
		job.prepare()
		job.getTarget().prepare()

		for host in job.getHosts():
			log.write("process host " + host.getID() , "notice")
			if host.prepare():
				for task in job.getTasks():
					if(job.getType() == "backup"):
						log.write("start task " + task.getName(), "debug")
						backup = Backup(job=job, source=host.getConnection(), target=job.getTarget().getConnection())
						backup.run(task)
					if(job.getType() == "dump"):
						log.write("start dump " + task.getName(), "debug")
						dump = Dump(job=job, source=host.getConnection(), target=job.getTarget().getConnection())
						dump.run(task)
			else:
				log.write("error: prepare host: " + host.getID() , "error")

		job.setLastRun()

	def runJob(self):
		job = Job().request()
		
		if not job:
			return False

		log.write("found job: " + job.getID() + " " + job.getName(), "notice")


		ret = job.apply()
		if ret == False:
			log.write("error apply as worker " + job.getWorker(), "notice")
		else:
			log.write("apply as worker " + job.getWorker(), "notice")
			return self.execJob(job)