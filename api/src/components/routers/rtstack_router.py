from fastapi import APIRouter, Depends

from ..dependencies import get_current_user
from ..redis.redis_client import rclient

router = APIRouter(prefix="/api/v1.0/ressources/rt-stack",
                   tags=["rtstack"],
                   dependencies=[Depends(get_current_user)],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/")
async def rtStack():
    return rclient.json().get('rt-stack')