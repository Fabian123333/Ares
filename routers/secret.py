from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from modules.parser import parseJson, parseOutput, shrinkJson
from modules.secret import Secret

router = APIRouter()

class Struct(BaseModel):
	id: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	secret: Optional[str] = None

@router.get("/", tags=["secret"])
async def get_all_secrets():
	ret = Secret().getAll()
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no secrets found")
	else:
		return parseJson(ret)

@router.post("/", tags=["secret"])
async def create_secret(data: Struct):
	id = Secret(data=data)
	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create secret")

@router.get("/{id}", tags=["secret"])
async def get_secret(id: str):
	ret = Secret(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="secret not found")
	else:
		return parseJson(ret)


@router.post("/query", tags=["secret"])
async def search_for_secrets(filter: Struct):
	ret = Secret().getAll(filter=shrinkJson(filter))
	return parseJson(ret)

@router.put("/{id}", tags=["secret"], response_model=Struct)
async def update_secret(id: str, item: Struct):
	secret = Secret(id)
	
	if not secret.exists():
		raise HTTPException(status_code=404, detail="secret not found")
	
	if not secret.update(item):
		raise HTTPException(status_code=422, detail="error update secret")
	
	return parseJson(secret)
	
@router.delete("/{id}", tags=["secret"])
async def delete_secret(id: str):
	ret = Secret(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="secret not found")
	else:
		return parseJson(ret)
