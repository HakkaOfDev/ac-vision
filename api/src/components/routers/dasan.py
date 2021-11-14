from fastapi import APIRouter, Depends
import requests
from ..dependencies import get_current_user


router = APIRouter(prefix="/api/v1.0/ressources/dasan",
                   tags=["dasan"],
                   dependencies=[Depends(get_current_user)],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/")
async def olt():
    pass

