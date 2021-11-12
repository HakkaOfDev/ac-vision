from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..tools.config.config_loader import config

DB_NAME = config["DB_NAME"]
DB_USER = config["DB_USER"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_HOST = config["DB_HOST"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True,
                       pool_recycle=3600,
                       connect_args={
                           "keepalives": 1,
                           "keepalives_idle": 30,
                           "keepalives_interval": 10,
                           "keepalives_count": 5,
                       })

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
