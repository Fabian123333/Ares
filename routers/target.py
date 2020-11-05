from bson import json_util
from fastapi import APIRouter, HTTPException
from typing import Optional

from modules.parser import parseJson, parseOutput
from modules.target import Target

router = APIRouter()

@router.get("/", tags=["target"])
async def getAll(filter: Optional[dict] = {}):
	ret = Target().getAll(filter)
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no targets found")
	else:
		return parseJson(ret)

@router.get("/{id}", tags=["target"])
async def get(id: str):
	ret = Target(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="target not found")
	else:
		return parseJson(ret)

@router.post("/", tags=["target"])
async def create(data: Target.StructNew):
	ret = Target(data=data)
	
	if ret:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create target")
	