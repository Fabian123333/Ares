from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from modules.task import Task
from modules.parser import parseJson, parseOutput, shrinkJson

router = APIRouter()

class Struct(BaseModel):
	id: Optional[str] = None
	name: Optional[str] = None
	type: Optional[str] = None # support file, database, partition
	description: Optional[str] = None
	data: Optional[dict] = None

	class Config:
		schema_extra = {
			"example": {
				"name": "Docker Backup",
				"type": "file",
				"data": {
					"container": ["dyndns_app"],
					"stacks": ["ares", "fhem", "swarmpit", "unifi"]
				}
			}
		}

@router.get("/", tags=["task"])
async def get_all_tasks(filter: Struct):
	ret = Task().getAll(filter)
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no tasks found")
	else:
		return parseJson(ret1)

@router.post("/query", tags=["task"], response_model=Struct)
async def search_for_tasks(filter: Struct):
	ret = Task().getAll(filter=shrinkJson(filter))
	return parseJson(ret)

@router.get("/{id}", tags=["task"], response_model=Struct)
async def get_task(id: str):
	ret = Task(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="task not found")
	else:
		return parseJson(ret)

@router.post("/", tags=["task"], response_model=Struct)
async def create_task(data: Struct):
	if(Task(name=data.name).exists()):
		raise HTTPException(status_code=422, detail="task already exist")
	
	ret = Task(data=data)

	if ret:
		return parseJson(ret)
	else:
		raise HTTPException(status_code=422, detail="can't create task")
		
@router.put("/{id}", tags=["task"], response_model=Struct)
async def update_task(id: str, item: Struct):
	task = Task(id)
	
	if not task.exists():
		raise HTTPException(status_code=404, detail="task not found")
	
	if not task.update(item):
		raise HTTPException(status_code=422, detail="error update task")
	
	return parseJson(task)

@router.delete("/{id}", tags=["task"])
async def delete_task(id: str):
	ret = Task(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="task not found")
	else:
		return parseJson(ret)
