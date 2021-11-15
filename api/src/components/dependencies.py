from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .sql_app import fonction
from pydantic import BaseModel
from typing import Optional

SECRET_KEY = "75f2a00ea3cedc3268f7a1e1b3106198b564dfb495273acba052161ce58db4de"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 1200

router = APIRouter(prefix="/api/v1.0/ressources/login",
                   tags=["login"], )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1.0/ressources/login/token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(fonction.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)
    except JWTError:
        raise credentials_exception
    user = fonction.get_user_by_login(db, login=token_data.login)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(fonction.get_db)):
    user = fonction.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password, please try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    content = {"message": "You're now logged in, welcome back ! Waiting for redirecting...", "acces_token": access_token}
    return content
