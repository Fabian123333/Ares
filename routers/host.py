from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from pydantic import BaseModel
from typing import Optional

from modules.parser import parseJson, parseOutput, shrinkJson
from modules.host import Host

router = APIRouter()

class Struct(BaseModel):
	id: Optional[str] = None
	hostname: Optional[str] = None
	description: Optional[str] = None
	credential_id: Optional[str] = None
	ip_address: Optional[str] = None
	type: Optional[str] = None # support linux, later support for windows 

@router.get("/", tags=["host"])
async def get_all_hosts():
	ret = Host().getAll()
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no hosts found")
	else:
		return parseJson(ret)

@router.post("/", tags=["host"])
async def create_host(data: Struct):
	ret = Host(data=data)
	
	if ret:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create host")

@router.get("/{id}", tags=["host"])
async def get_host(id: str):
	ret = Host(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="host not found")
	else:
		return parseJson(ret)


@router.post("/query", tags=["host"])
async def search_for_hosts(filter: Struct):
	ret = Host().getAll(filter=shrinkJson(filter))
	return parseJson(ret)

@router.put("/{id}", tags=["host"], response_model=Struct)
async def update_host(id: str, item: Struct):
	host = Host(id)
	
	if not host.exists():
		raise HTTPException(status_code=404, detail="host not found")
	
	if not host.update(item):
		raise HTTPException(status_code=422, detail="error update host")
	
	return parseJson(host)
	
@router.delete("/{id}", tags=["host"])
async def delete_host(id: str):
	ret = Host(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="host not found")
	else:
		return parseJson(ret)

@router.get("/check/{id}", tags=["host"], response_model=Struct)
async def check_host_connection(id: str):
	host = Host(id)
	
	if ( host.Connect() == False ):
		raise HTTPException(status_code=422, detail="host connection not possible")
	else: 
		return parseJson(host)
