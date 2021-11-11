from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import login
from ..sql_app import fonction, schemas

router = APIRouter(prefix="/items",
                   tags=["items"],
                   dependencies=[Depends(login)],
                   responses={404: {"description": "Not found"}},
                   )


@router.get("/api/v1/ressources/users/")
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(fonction.get_db)):
    users = fonction.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/api/v1/ressources/users/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(fonction.get_db)):
    if fonction.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already taken")
    if fonction.get_user_by_login(db, login=user.login):
        raise HTTPException(status_code=400, detail="login already taken")
    return fonction.create_user(db, user=user)
