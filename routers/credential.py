from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from modules.parser import parseJson, parseOutput, shrinkJson
from modules.credential import Credential

router = APIRouter()

class Struct(BaseModel):
	id: Optional[str] = None
	name: Optional[str] = None
	type: Optional[str] = None # support certificate, token, none and password
	username: Optional[str] = None
	description: Optional[str] = None
	secret_id: Optional[str] = None

@router.get("/", tags=["credential"])
async def get_all_credentials():
	ret = Credential().getAll()
		
	if ( len(ret) == 0 ):
		raise HTTPException(status_code=404, detail="no credentials found")
	else:
		return parseJson(ret)

@router.get("/{id}", tags=["credential"], response_model=Struct)
async def get_credential(id: str):
	ret = Credential(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="credential not found")
	else:
		return parseJson(ret)

@router.post("/", tags=["credential"])
async def create_credential(data: Struct):
	ret = Credential(data=data)
	
	if ret:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create credential")

@router.post("/query", tags=["credential"])
async def search_for_credentials(filter: Struct):
	ret = Credential().getAll(filter=shrinkJson(filter))
	return parseJson(ret)
		
@router.put("/{id}", tags=["credential"], response_model=Struct)
async def update_credential(id: str, item: Struct):
	credential = Credential(id)
	
	if not credential.exists():
		raise HTTPException(status_code=404, detail="credential not found")
	
	if not credential.update(item):
		raise HTTPException(status_code=422, detail="error update credential")
	
	return parseJson(credential)

@router.delete("/{id}", tags=["credential"])
async def delete_credential(id: str):
	ret = Credential(id).delete()
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="credential not found")
	else:
		return parseJson(ret)
