from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, login: str, password: str):
    user = get_user_by_login(db, login)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.Users).filter(models.Users.login == login).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def hash_password(password: str):
    return pwd_context.hash(password)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    login = user.last_name[0].lower() + user.first_name.lower()
    db_user = models.Users(first_name=user.first_name, last_name=user.last_name, login=login, email=user.email,
                           password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, login: str):
    login = get_user_by_login(db, login)
    db.delete(login)
    db.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_onusd(db: Session, onuid: int):
    desc = db.query(models.Onus).filter(models.Onus.onuid == onuid).first()
    if desc == None:
        return ""
    else:
        return desc.description

def set_onusd(db: Session, onu: schemas.Onusd):
    if get_onusd(db, onu.onuid):
        db_onu = db.query(models.Onus).filter(models.Onus.onuid == onu.onuid).first()
        setattr(db_onu, "descrption", onu.description)
    else:
        db_onu = models.Onus(onuid=onu.onuid, description=onu.description)
    db.add(db_onu)
    db.commit()
    db.refresh(db_onu)
    return db_onu


def get_setting(db: Session, name: str):
    return db.query(models.Setting).filter(models.Setting.name == name).first()


def set_setting(db: Session, setting: schemas.Setting):
    set = models.Setting(name=setting.name, value=setting.value)
    db.add(set)
    db.commit()
    db.refresh(set)
    return set
