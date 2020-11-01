from bson import json_util
from fastapi import APIRouter, HTTPException

from modules import secret

router = APIRouter()

@router.get("/", tags=["secret"])
async def get():
	secrets = secret.getAll()
	if ( len(secrets) == 0 ):
		raise HTTPException(status_code=404, detail="no secrets found")
	else:		
		return json_util.dumps(secrets,default=json_util.default)

@router.post("/", tags=["secret"])
async def create(data: secret.StructNew):
	id = secret.create(data)
	
	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create secret")
	