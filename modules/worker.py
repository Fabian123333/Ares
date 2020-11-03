from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import job, host, target, task

from modules.backup import Backup

class worker():
	def __init__(self):
		log.write("init worker", "debug")
		self.uuid:str = None

	def getJob(self):
		return job.request()

	def prepareSource(self):
		pass

	def execJob(self):
		log.write("exec job " + self.id , "notice")
		# job.start(self.job["_id"])
		t = target.prepare(self.job["target_id"])

		for h_id in self.job["host_ids"]:
			log.write("process host " + h_id , "notice")
			h = host.prepare(h_id)
			
			for t_id in self.job["task_ids"]:
				cur_task = task.get(t_id)
				if(self.job["type"] == "backup"):
					log.write("start task " + self.job["name"], "debug")
					backup = Backup(self.job, h, t)
					backup.run(cur_task)

		job.finish(str(self.job["_id"]))

	def runJob(self):
		self.job = self.getJob()
		if not self.job:
			return False
		if "name" in self.job:
			id = str(self.job["_id"])
			log.write("found job: " + id + " " + self.job["name"])
			worker_id = job.apply(id)
			if not worker_id:
				return False
			
			log.write("apply as worker " + worker_id, "notice")
			self.id = worker_id
			return self.execJob()