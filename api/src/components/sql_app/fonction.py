from webbrowser import get
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



#Fonctions for user router
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

#Fonction for all router to get the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#Fonctions for dasan router onus description set and get        
def get_onusd(db: Session, onuid: int):
    desc = db.query(models.Onus).filter(models.Onus.onuid == onuid).first()
    if desc == None:
        return ""
    else:
        return desc.description

def set_onusd(db: Session, onu: schemas.Onusd):
    if get_onusd(db, onu.onuid):
        db_onu = db.query(models.Onus).filter(models.Onus.onuid == onu.onuid).first()
        setattr(db_onu, "description", onu.description)
    else:
        db_onu = models.Onus(onuid=onu.onuid, description=onu.description)
    db.add(db_onu)
    db.commit()
    db.refresh(db_onu)
    return db_onu

#Fonctions for dasan router setting set and get 
def get_setting(db: Session, name: str):
    return db.query(models.Setting).filter(models.Setting.name == name).first()


def set_setting(db: Session, setting: schemas.Setting):
    if get_setting(db, setting.name):
        set = db.query(models.Setting).filter(models.Setting.name == setting.name).first()
        setattr(set, "value", setting.value)
    else:
        set = models.Setting(name=setting.name, value=setting.value)
    db.add(set)
    db.commit()
    db.refresh(set)
    return set

#Fonctions for notification router
def get_notification(db: Session, skip: int = 0, limit: int = 100):
    notifications = db.query(models.Notification).offset(skip).limit(limit).all()
    notifications.date.sort(key=lambda date: datetime.strptime(date, "%-m-%-d-%Y, %H:%M,%S"))
    return notifications

def post_notification(db: Session, notification: schemas.Notification):
    db_notif = models.Notification(onuid=int(notification.onuid), gponPort=int(notification.gponPort),
                                   reason=('', notification.reason)[notification.reason is not None], status=notification.status, date=notification.date)
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif


def del_notification(db: Session, id: int):
    notif = db.query(models.Notification).filter(models.Notification.id == id).first()
    db.delete(notif)
    db.commit()
    return "Notification delete"
    