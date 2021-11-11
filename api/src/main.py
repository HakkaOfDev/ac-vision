import urllib3
import uvicorn
from fastapi import FastAPI
from components.sql_app import models
from components.dependencies import *
from components.routers import users, ubiquiti
from components.sql_app.database import engine

app = FastAPI()

app.include_router(router)
app.include_router(users.router)
app.include_router(ubiquiti.router)

models.Base.metadata.create_all(bind=engine)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port="8000")
