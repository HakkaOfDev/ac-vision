from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from ..sql_app import fonction, schemas


router = APIRouter(prefix="/api/v1.0/ressources/notification",
                   tags=["notification"],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/")
async def get_notification(skip: int = 0, limit: int = 100, db: Session = Depends(fonction.get_db)):
    return fonction.get_notification(db, skip, limit)


router.post("/")
async def post_notification(notification: schemas.Notification, db: Session = Depends(fonction.get_db)):
    return fonction.post_notification(db, notification)