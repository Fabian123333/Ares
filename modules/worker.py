from pydantic import BaseModel
from typing import Optional

from core import db
from core import log

from modules import job

class worker():
	def __init__(self):
		log.write("init worker", "debug")
		self.uuid:str = None

	def getJob(self):
		job.
		  