import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from sql_app import fonction, models, schemas
from sql_app.database import SessionLocal, engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token, db: Session = Depends(get_db)):
    if token in db:
        user = fonction.get_user_by_login(db, token)
        return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/login/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = fonction.get_user_by_login(db, form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not pwd_context.verify(form_data.password, user_dict.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": {"first_name": user_dict.first_name, "last_name": user_dict.last_name, "role": user_dict.role},
        "token_type": "bearer"}


@app.get("/api/v1/ressources/users/")
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = fonction.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/api/v1/ressources/users/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if fonction.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already taken")
    if fonction.get_user_by_login(db, login=user.login):
        raise HTTPException(status_code=400, detail="login already taken")
    return fonction.create_user(db, user=user)


@app.get("/")
async def root():
    return {"message": "Bienvenue !"}


# /api/v1/ressources/olt-[du]/onu/id_onu


@app.get("/api/v1/ressources/")
async def home():
    return {"message": "Bienvenue dans l'api V1 ! ^^"}


@app.get("/api/v1/ressources/olt-d/onu/{onu_id}")
async def get_onu(onu_id: int):
    return {"result": onu_id}


@app.get("/api/v1/ressources/olt-u/onu/{onu_id}")
async def get_onu(onu_id: int):
    return {"result": onu_id}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port="8000")
