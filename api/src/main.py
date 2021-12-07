import urllib3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from components.sql_app import models
from components.dependencies import router
from components.routers import users, ubiquiti, dasan, rtstack
from components.sql_app.database import engine

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.include_router(router)
app.include_router(users.router)
app.include_router(ubiquiti.router)
app.include_router(dasan.router)
app.include_router(rtstack.router)

models.Base.metadata.create_all(bind=engine)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

origins = [
    "http://ac-vision",
    "http://ac-vision.chalons.univ-reims.fr"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#if __name__ == "__main__":
    #uvicorn.run(app, host="127.0.0.1", port="8000")
