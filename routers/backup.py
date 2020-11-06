from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from modules.parser import parseJson, parseOutput, shrinkJson
from modules.backup import Backup

router = APIRouter()

class Struct(BaseModel):
	id: Optional[str] = None
	file: Optional[str] = None 
	job_id: Optional[str] = None
	task_id: Optional[str] = None
	host_id: Optional[str] = None
	target_id: Optional[str] = None
	hostname: Optional[str] = None
	log: Optional[str] = None
	start_time: Optional[str] = None
	end_time: Optional[str] = None


@router.get("/", tags=["backup"])
async def get_all_backups():
	ret = Backup().getAll()
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no backups found")
	else:
		return parseJson(ret)

@router.get("/{id}", tags=["backup"], response_model=Struct)
async def get_backup(id: str):
	ret = Backup(id)
	if ( ret.exists() == False ):
		raise HTTPException(status_code=404, detail="backup not found")
	else:
		return parseJson(ret)

@router.delete("/{id}", tags=["backup"])
async def delete_backup(id: str):
	ret = Backup(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="backup not found")
	else:
		return {"status": "success"}

@router.get("/restore/{id}", tags=["backup"])
async def restore_backup(id: str):
	backup = Backup(id)
	ret = backup.restore()
	return {"status": "success"}
	
@router.post("/query", tags=["backup"])
async def search_for_backups(filter: Struct):
	ret = Backup().getAll(filter=shrinkJson(filter))
	return parseJson(ret)
