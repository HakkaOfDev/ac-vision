from fastapi import APIRouter
from ..redis.redis_client import rclient

router = APIRouter(prefix="/api/v1.0/ressources/devices",
                   tags=["devices"],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/")
async def devices():
    devices = []
    olt = rclient.json().get('olt-dasan')
    onus = rclient.json().get('onus-dasan')
    devices.append(olt)
    devices.append(onus)
    return devices