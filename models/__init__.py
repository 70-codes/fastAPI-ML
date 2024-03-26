from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String)
    lname = Column(String)
    email = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    password = Column(String)
    is_admin = Column(Boolean, default=0)

    models = relationship("Models", back_populates="owner")


class Models(Base):
    __tablename__ = "Models"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String)

    owner = relationship("User", back_populates="models")
    pass
