from pydantic import BaseModel
from typing import Optional
from time import sleep

from core import db
from core import log

from config import worker as config
from modules.worker import worker

class main_loop():
	def __init__(self):
		self.worker = worker()

	def run(self):
		while True:
			worker.
			sleep(conf.interval)
			