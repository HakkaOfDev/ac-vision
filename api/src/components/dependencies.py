from fastapi import HTTPException, APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .sql_app import fonction

router = APIRouter(prefix="/api/v1.0/ressources/logins",
                   tags=["logins"], )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_token_header(x_token: str = Header(...)):
    pass


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(fonction.get_db)):
    user_dict = fonction.get_user_by_login(db, form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not pwd_context.verify(form_data.password, user_dict.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": {"first_name": user_dict.first_name, "last_name": user_dict.last_name, "role": user_dict.role},
        "token_type": "bearer"}
