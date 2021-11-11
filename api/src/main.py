import uvicorn
from fastapi import FastAPI
from components.sql_app import models
from components.dependencies import *
from components.routers import users, ubiquiti
from components.sql_app.database import engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/")

app.include_router(router)
app.include_router(users.router)
app.include_router(ubiquiti.router)

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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port="8000")
