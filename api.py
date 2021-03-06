from typing import Optional
from fastapi import Depends, FastAPI, Header, HTTPException

from routers import secret, host, credential, target, job, task, backup, dump
app = FastAPI()

# x_token: str = Header(...)
async def get_token_header():
	pass
    #if x_token != "fake-super-secret-token":
    #    raise HTTPException(status_code=400, detail="X-Token header invalid")

#app.include_router(secret.router)

app.include_router(backup.router,
	prefix="/backup",tags=["backup"],dependencies=[Depends(get_token_header)],responses={404: {"description": "Not found"}})

app.include_router(credential.router,
	prefix="/credential",tags=["credential"],dependencies=[Depends(get_token_header)],responses={404: {"description": "Not found"}})

app.include_router(dump.router,
	prefix="/dump",tags=["dump"],dependencies=[Depends(get_token_header)],responses={404: {"description": "Not found"}})

app.include_router(host.router,
	prefix="/host",tags=["host"],dependencies=[Depends(get_token_header)],	responses={404: {"description": "Not found"}})

app.include_router(job.router,
	prefix="/job",tags=["job"],dependencies=[Depends(get_token_header)],responses={404: {"description": "Not found"}})

app.include_router(secret.router,
	prefix="/secret",tags=["secret"],dependencies=[Depends(get_token_header)],responses={404: {"description": "Not found"}})

app.include_router(target.router,
	prefix="/target",tags=["target"],dependencies=[Depends(get_token_header)],responses={404: {"description": "Not found"}})

app.include_router(task.router,
	prefix="/task",tags=["task"],dependencies=[Depends(get_token_header)],responses={404: {"description": "Not found"}})
