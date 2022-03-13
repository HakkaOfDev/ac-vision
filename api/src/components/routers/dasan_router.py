from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..dependencies import get_current_user
from ..redis.redis_client import rclient
from ..handlers.dasan_handler import DasanWorkflow
from ..sql_app import fonction, schemas
from sqlalchemy.orm import Session

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
async def nameonu(onu: schemas.Onusd, db: Session = Depends(fonction.get_db)):
    return fonction.set_onusd(db, onu=onu)

@router.patch("/desconu")
async def nameonu(onu: schemas.Onusd, db: Session = Depends(fonction.get_db)):
    return fonction.set_onusd(db, onu=onu)

@router.get("/desconu")
async def getdesconu(onuid: int ,db: Session = Depends(fonction.get_db)):
    return fonction.get_onusd(db, onuid)


@router.get("/onuactivity")
async def getonuactivity():
    return rclient.json().get('onus-activity')


@router.post("/setting")
async def setipolt(setting: schemas.Setting, db: Session = Depends(fonction.get_db)):
    return fonction.set_setting(db, setting=setting)


@router.get("/setting")
async def getoltip(name: str, db: Session = Depends(fonction.get_db)):
    return fonction.get_setting(db, name)