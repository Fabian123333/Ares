from bson import json_util
from bson.json_util import dumps, loads
from fastapi import APIRouter, HTTPException
from modules import target, job, host, task
from core.db import parseOutput

router = APIRouter()

@router.get("/", tags=["job"])
async def getAll():
	jobs = job.getAll()
	if ( len(jobs) == 0 ):
		raise HTTPException(status_code=404, detail="no jobs found")
	else:
		return parseOutput(jobs)

@router.get("/{job_id}", tags=["job"])
async def apply(job_id: str):
	ret = job.apply(job_id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="job not found or already claimed")
	else:
		return {"worker": ret, "job": job_id}

@router.get("/request/", tags=["job"])
async def request():
	jobs = job.request()
	if ( jobs == False ):
		raise HTTPException(status_code=404, detail="no jobs available")
	else:
		return parseOutput(jobs)

@router.delete("/{job_id}", tags=["job"])
async def delete(job_id: str):
	ret = job.delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="job not found")
	else:

		return parseOutput(ret)

@router.post("/", tags=["job"])
async def create(data: job.StructJobNew):

	if(job.getByName(data.name)):
		raise HTTPException(status_code=422, detail="job already exist")

	for id in data.host_ids:
		if not host.exists(id):
			raise HTTPException(status_code=422, detail="host does not exist")


	for id in data.task_ids:
		if not task.exists(id):
			raise HTTPException(status_code=422, detail="task does not exist")
	

	if not target.exists(data.target_id):
		raise HTTPException(status_code=422, detail="target does not exist")
	
	id = job.create(data)

	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create target")
	