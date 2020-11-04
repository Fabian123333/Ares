from bson import json_util
from fastapi import APIRouter, HTTPException
from modules.task import Task


from modules.parser import parseJson, parseOutput

router = APIRouter()

@router.get("/", tags=["task"])
async def getAll(filter: Task.StructTaskFilter):
	if(hasattr(filter, "filter")):
		tasks = Task().getAll(filter.filter)
	else:
		tasks = Task().getAll()
		
	if ( len(tasks) == 0 ):
		raise HTTPException(status_code=404, detail="no tasks found")
	else:
		return parseJson(tasks)

@router.get("/{id}", tags=["task"])
async def get(id: str):
	ret = Task(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="task not found")
	else:
		return parseJson(ret)

@router.post("/", tags=["task"])
async def create(data: Task.StructTaskNew):
	if(task.getByName(data.name)):
		raise HTTPException(status_code=422, detail="task already exist")
	
	id = Task(data)

	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create task")
	