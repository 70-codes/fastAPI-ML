from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

SQLALCHEMY_DATABASE_URL = "sqlite:///./project.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_pd_db():
    df = pd.read_csv(
        "/home/creed347/Desktop/.dev/final_project/fastapi/ml-dataset/cvm_indicators_dataset_2011-2021.csv"
    )
    return df
    pass
