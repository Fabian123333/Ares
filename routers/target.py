from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from modules.parser import parseJson, parseOutput, shrinkJson
from modules.target import Target

router = APIRouter()

class Struct(BaseModel):
	id: Optional[str] = None
	hostname: Optional[str] = None
	credential_id: Optional[str] = None
	description: Optional[str] = None
	ip_address: Optional[str] = None
	type: Optional[str] = None # support linux, later support for windows 
	location: Optional[str] = None
	path: Optional[str] = None

@router.post("/query", tags=["target"])
async def search_for_target(filter: Struct):
	ret = Target().getAll(filter=shrinkJson(filter))
	return parseJson(ret)

@router.get("/", tags=["target"])
async def get_all_targets():
	ret = Target().getAll()
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no targets found")
	else:
		return parseJson(ret)

@router.get("/{id}", tags=["target"])
async def get_target(id: str):
	ret = Target(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="target not found")
	else:
		return parseJson(ret)

@router.post("/", tags=["target"])
async def create_target(data: Struct):
	ret = Target(data=data)
	
	if ret:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create target")
		
@router.put("/{id}", tags=["target"], response_model=Struct)
async def update_target(id: str, item: Struct):
	target = Target(id)
	
	if not target.exists():
		raise HTTPException(status_code=404, detail="target not found")
	
	if not target.update(item):
		raise HTTPException(status_code=422, detail="error update target")
	
	return parseJson(target)

@router.delete("/{id}", tags=["target"])
async def delete_target(id: str):
	ret = Target(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="target not found")
	else:
		return parseJson(ret)
