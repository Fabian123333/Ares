from bson import json_util
from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from modules import host

router = APIRouter()

@router.get("/", tags=["host"])
async def getAll():
	hosts = host.getAll()
	if ( len(hosts) == 0 ):
		raise HTTPException(status_code=404, detail="no hosts found")
	else:
		return json_util.dumps(hosts,default=json_util.default)

@router.get("/{id}", tags=["host"])
async def get(id: str):
	ret = host.get(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="host not found")
	else:
		return json_util.dumps(ret,default=json_util.default)

@router.post("/", tags=["host"])
async def create(data: host.StructHostNew):
	id = host.create(data)
	
	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create credential")
	