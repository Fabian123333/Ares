from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import host, target

from modules.job import Job
from modules.task import Task

from modules.backup import Backup

class worker():
	def __init__(self):
		log.write("init worker", "debug")
		self.uuid:str = None

	def prepareSource(self):
		pass

	def execJob(self, job):
		log.write("exec job " + job.id , "notice")
		# job.setStatus("started")
		t = target.prepare(job.getTarget())

		for h_id in job.getHosts():
			log.write("process host " + h_id , "notice")
			h = host.prepare(h_id)
			
			for t_id in job.getTasks():
				cur_task = Task(t_id)
				if(job.getType() == "backup"):
					log.write("start task " + cur_task.getName(), "debug")
					backup = Backup(job, h, t)
					backup.run(cur_task)

		# job.finish(str(self.job["_id"]))

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