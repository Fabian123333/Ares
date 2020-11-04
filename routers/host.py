from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from typing import Optional

from modules.parser import parseJson, parseOutput
from modules.host import Host

router = APIRouter()

@router.get("/", tags=["host"])
async def getAll(filter: Optional[dict] = {}):
	ret = Host().getAll(filter)
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no hosts found")
	else:
		return parseJson(ret)

@router.get("/{id}", tags=["host"])
async def get(id: str):
	ret = Host(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="host not found")
	else:
		return parseJson(ret)

@router.post("/", tags=["host"])
async def create(data: Host.StructNew):
	ret = Host(data=data)
	
	if ret:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create host")
	