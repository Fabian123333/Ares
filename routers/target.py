from bson import json_util
from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from modules import target, credential

router = APIRouter()

@router.get("/", tags=["target"])
async def getAll():
	targets = target.getAll()
	if ( len(targets) == 0 ):
		raise HTTPException(status_code=404, detail="no targets found")
	else:
		return json_util.dumps(targets,default=json_util.default)

@router.get("/{id}", tags=["target"])
async def get(id: str):
	ret = target.get(id)
	if ( ret == False ):
		raise HTTPException(status_code=404, detail="target not found")
	else:
		return json_util.dumps(ret,default=json_util.default)

@router.post("/", tags=["target"])
async def create(data: target.StructNew):

	if(target.getByName(data.name)):
		raise HTTPException(status_code=422, detail="target already exist")

	if(not credential.exists(data.credential_id)):
		raise HTTPException(status_code=422, detail="credential_id not found")

	id = target.create(data)

	if id:
		return {"state": "true"}
	else:
		raise HTTPException(status_code=422, detail="can't create credential")

