from telnetlib import STATUS
from fastapi import APIRouter, Depends, HTTPException

from api.src.components.redis.cache_updates import update_cache

from ..dependencies import get_current_user
from ..handlers.map_handler import MapWorkflow

router = APIRouter(prefix="/api/v1.0/ressources/map",
                   tags=["map"],
                   dependencies=[Depends(get_current_user)],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/")
async def map():
    map_workflow = MapWorkflow()
    map_workflow.build()
    if map_workflow.get() is None:
        raise HTTPException(status_code=404, detail='An error occured, please contact an administrator.')
    return map_workflow.get()

@router.get("/update")
async def update():
    update_cache()
    return 'Cache updated'
