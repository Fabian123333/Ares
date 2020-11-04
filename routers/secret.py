from fastapi import APIRouter, HTTPException
from bson import json_util
from typing import Optional

from modules.parser import parseJson, parseOutput
from modules.secret import Secret

router = APIRouter()

@router.get("/", tags=["secret"])
async def getAll(filter: Optional[dict] = {}):
	ret = Secret().getAll(filter)
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no secrets found")
	else:
		return parseJson(ret)

@router.post("/", tags=["secret"])
async def create(data: Secret.StructNew):
	id = Secret(data=data)
	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create secret")
	