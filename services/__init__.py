import models
from database import engine


def create_db():
    models.Base.metadata.create_all(bind=engine)
