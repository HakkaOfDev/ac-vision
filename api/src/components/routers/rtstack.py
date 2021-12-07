from fastapi import APIRouter, Depends

from ..dependencies import get_current_user

router = APIRouter(prefix="/api/v1.0/ressources/rt-stack",
                   tags=["rtstack"],
                   dependencies=[Depends(get_current_user)],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/")
async def rtStack():
    rt_stack = {
        "ipAddress": "10.59.10.1",
        "status": "active",
        "uptime": "Test",
        "temperature": "10",
        "macAddress": "13:54:65:ed:fe:32",
        "displayName": "RT-Stack",
        "site": {
            "name": "IUT CHALONS"
        }
    }
    return rt_stack
