from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..dependencies import get_current_user
from ..redis.redis_client import rclient
from ..handlers.dasan_handler import DasanWorkflow

class Onudesc(BaseModel):
    onuid: int
    desc: str

router = APIRouter(prefix="/api/v1.0/ressources/dasan",
                   tags=["dasan"],
                   dependencies=[Depends(get_current_user)],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/olt")
async def olt():
    return rclient.json().get('olt-dasan')


@router.get("/onus")
async def onus():
    return rclient.json().get('onus-dasan')

@router.post("/desconu")
async def nameonu(onudesc: Onudesc):
    dasan_workflow = DasanWorkflow('10.59.10.20')
    dasan_workflow.set_onu_desc(onudesc.onuid, onudesc.desc)
    return "Nom changé"