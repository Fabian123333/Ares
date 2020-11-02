from bson import json_util
from fastapi import APIRouter, HTTPException

from modules import credential

router = APIRouter()

@router.get("/", tags=["credential"])
async def getCredentials():
	credentials = credential.getAll()
	if ( len(credentials) == 0 ):
		raise HTTPException(status_code=404, detail="no credentials found")
	else:
		return json_util.dumps(credentials,default=json_util.default)

@router.get("/{id}", tags=["credential"])
async def get(id: str):
	ret = credential.get(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="credential not found")
	else:
		return json_util.dumps(ret,default=json_util.default)

@router.post("/", tags=["credential"])
async def create(data: credential.StructNew):
	id = credential.create(data)
	
	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create credential")
	