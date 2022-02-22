import urllib3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from components.tools.log_listener import listener
from components.tools.log_listener import server
from components.redis.cache_updates import run_cache
from components.dependencies import router
from components.routers import users_router, ubiquiti_router, dasan_router, rtstack_router, map_router
from components.sql_app import models
from components.sql_app.database import engine
import uvicorn
from multiprocessing import Process
import threading

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.include_router(router)
app.include_router(users_router.router)
app.include_router(ubiquiti_router.router)
app.include_router(dasan_router.router)
app.include_router(rtstack_router.router)
app.include_router(map_router.router)

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    server.run_forever(threaded=True)

    threading.Thread(target=listener).start()
    print('listener on')
    run_cache()