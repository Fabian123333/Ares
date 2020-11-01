from bson import json_util
from fastapi import APIRouter, HTTPException
from modules import target, job, host, task

router = APIRouter()

@router.get("/", tags=["job"])
async def getAll():
	jobs = job.getAll()
	if ( len(jobs) == 0 ):
		raise HTTPException(status_code=404, detail="no jobs found")
	else:
		return json_util.dumps(jobs,default=json_util.default)

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
	