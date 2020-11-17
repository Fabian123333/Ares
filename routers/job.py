from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from modules.job import Job
from modules.task import Task
from modules.target import Target
from modules.host import Host
from modules.worker import Worker
from modules.parser import parseJson, parseOutput

router = APIRouter()

class Struct(BaseModel):
	id: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	type: Optional[str] = None
	snapshots: Optional[int] = None
	interval: Optional[int] = None # interval in minutes
	target_id: Optional[str] = None
	host_ids: Optional[list] = None
	task_ids: Optional[list] = None

@router.get("/", tags=["job"])
async def get_all_jobs():
	jobs = Job().getAll()
	if ( len(jobs) == 0 ):
		raise HTTPException(status_code=404, detail="no jobs found")
	else:
		return parseJson(jobs)

@router.put("/{id}", tags=["job"], response_model=Struct)
async def update_job(id: str, item: Struct):
	job = Job(id)
	
	if not job:
		raise HTTPException(status_code=404, detail="job not found")
	
	if not job.update(item):
		raise HTTPException(status_code=422, detail="error update Job")
	
	return parseJson(job)

@router.get("/{id}", tags=["job"], response_model=Struct)	
async def get_job(id: str):
	job = Job(id)
	
	if(job.exists() == False):
		raise HTTPException(status_code=404, detail="job not found")
	else:
		return parseJson(job)

@router.get("/apply/{id}", tags=["job"])
async def apply_for_job(id: str):
	ret = Job(id).apply()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="job not found or already claimed")
	else:
		return parseJson(ret)

@router.get("/run/{id}", tags=["job"])
async def run_job(id: str):
	job = Job(id)
	if not job.exists():
		raise HTTPException(status_code=404, detail="job not found or already claimed")
	worker = Worker()
	worker.execJob(job)
	return {"status": "success"}

@router.get("/request/", tags=["job"])
async def request_job():
	jobs = Job().request()
	if ( jobs == False ):
		raise HTTPException(status_code=404, detail="no jobs available")
	else:
		return parseJson(jobs)

@router.post("/", tags=["job"])
async def create_job(data: Struct):

	if(Job(name=data.name).exists()):
		raise HTTPException(status_code=422, detail="job already exist")

	for id in data.host_ids:
		if not Host(id):
			raise HTTPException(status_code=422, detail="host does not exist")


	for id in data.task_ids:
		if not Task(id):
			raise HTTPException(status_code=422, detail="task does not exist")
	

	if not Target(data.target_id):
		raise HTTPException(status_code=422, detail="target does not exist")

	j = Job(data=data)

	if j.getID():
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create target")

@router.delete("/{id}", tags=["job"])
async def delete_job(id: str):
	ret = Job(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="job not found")
	else:
		return True