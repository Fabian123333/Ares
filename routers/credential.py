from bson import json_util
from fastapi import APIRouter, HTTPException
from typing import Optional

from modules.parser import parseJson, parseOutput
from modules.credential import Credential

router = APIRouter()

@router.get("/", tags=["credential"])
async def getAll(filter: Optional[dict] = {}):
	ret = Credential().getAll(filter)
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no credentials found")
	else:
		return parseJson(ret)

@router.get("/{id}", tags=["credential"])
async def get(id: str):
	ret = Credential(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="credential not found")
	else:
		return parseJson(ret)

@router.post("/", tags=["credential"])
async def create(data: Credential.StructNew):
	ret = Credential(data=data)
	
	if ret:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create credential")
	