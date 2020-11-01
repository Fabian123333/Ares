from bson import json_util
from fastapi import APIRouter, HTTPException
from modules import task

router = APIRouter()

@router.get("/", tags=["task"])
async def getAll():
	tasks = task.getAll()
	if ( len(tasks) == 0 ):
		raise HTTPException(status_code=404, detail="no tasks found")
	else:
		return json_util.dumps(tasks,default=json_util.default)

@router.post("/", tags=["task"])
async def create(data: task.StructTaskNew):

	if(task.getByName(data.name)):
		raise HTTPException(status_code=422, detail="task already exist")
	
	id = task.create(data)

	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create task")
	