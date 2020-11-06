from pydantic import BaseModel
from typing import Optional
from time import sleep
from core import db
from core import log

from config import worker as conf
from modules.worker import Worker

class main_loop():
	def __init__(self):
		self.worker = Worker()

	def run(self):
		log.write("start worker")
		while True:
			self.worker.runJob()
			sleep(conf["interval"])

loop = main_loop()
loop.run()