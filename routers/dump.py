from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from modules.parser import parseJson, parseOutput, shrinkJson
from modules.dump import Dump

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


@router.get("/", tags=["dump"])
async def get_all_dumps():
	ret = Dump().getAll()
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no dumps found")
	else:
		return parseJson(ret)

@router.get("/{id}", tags=["dump"], response_model=Struct)
async def get_dump(id: str):
	ret = Dump(id)
	if ( ret.exists() == False ):
		raise HTTPException(status_code=404, detail="dump not found")
	else:
		return parseJson(ret)

@router.delete("/{id}", tags=["dump"])
async def delete_dump(id: str):
	ret = Dump(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="dump not found")
	else:
		return {"status": "success"}

#@router.get("/restore/{id}", tags=["dump"])
#async def restore_dump(id: str):
#	dump = Dump(id)
#	ret = dump.restore()
#	return {"status": "success"}

@router.post("/query", tags=["dump"])
async def search_for_dumps(filter: Struct):
	ret = Dump().getAll(filter=shrinkJson(filter))
	return parseJson(ret)
