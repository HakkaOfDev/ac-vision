from fastapi import APIRouter, Depends

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
    return map_workflow.get()
