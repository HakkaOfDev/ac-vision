from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_current_user
from ..sql_app import fonction, schemas

router = APIRouter(prefix="/api/v1.0/ressources/users",
                   tags=["users"],
                   dependencies=[Depends(get_current_user)],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/")
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(fonction.get_db)):
    users = fonction.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(fonction.get_db)):
    if fonction.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already taken")
    return fonction.create_user(db, user=user)
