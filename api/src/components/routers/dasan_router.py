from fastapi import APIRouter, Depends

from ..dependencies import get_current_user
from ..redis.redis_client import rclient

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
