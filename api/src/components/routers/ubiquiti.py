from fastapi import APIRouter, Depends
from ..dependencies import login

router = APIRouter(prefix="/ubiquiti",
                   tags=["ubiquiti"],
                   dependencies=[Depends(login)],
                   responses={404: {"description": "Not found"}},
                   )


@router.get("/olt-u")
async def test():
    return {"message": "test good"}

