from bson import json_util
from bson.json_util import dumps, loads
from fastapi import APIRouter, HTTPException
from modules import target, host, task
from core.db import parseOutput, parseJson

from modules.job import Job

router = APIRouter()

@router.get("/", tags=["job"])
async def getAll():
	jobs = Job().getAll("json")
	if ( len(jobs) == 0 ):
		raise HTTPException(status_code=404, detail="no jobs found")
	else:
		return parseJson(jobs)

@router.get("/{job_id}", tags=["job"])
async def apply(id: str):
	ret = Job(id).apply()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="job not found or already claimed")
	else:
		return {"worker": ret, "job": id}

@router.get("/request/", tags=["job"])
async def request():
	jobs = Job().request()
	if ( jobs == False ):
		raise HTTPException(status_code=404, detail="no jobs available")
	else:
		return parseJson(jobs)

@router.delete("/{id}", tags=["job"])
async def delete(id: str):
	ret = Job(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="job not found")
	else:

		return parseOutput(ret)

@router.post("/", tags=["job"])
async def create(data: Job.StructNew):

	if(Job(name=data.name).exists()):
		raise HTTPException(status_code=422, detail="job already exist")

	for id in data.host_ids:
		if not host.exists(id):
			raise HTTPException(status_code=422, detail="host does not exist")


	for id in data.task_ids:
		if not task.exists(id):
			raise HTTPException(status_code=422, detail="task does not exist")
	

	if not target.exists(data.target_id):
		raise HTTPException(status_code=422, detail="target does not exist")

	j = job.create(data=data)

	if j.getId():
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create target")
	