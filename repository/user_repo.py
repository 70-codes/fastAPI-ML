from models import User
from datetime import datetime
from authentication.hash import Hash
from fastapi import status, HTTPException


def get_user_by_email(request, db):
    email = request.email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        pass
    return user
    pass


def get_user_by_id(id: int, db):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    return user
    pass


def create_user(request, db):
    user = get_user_by_email(request=request, db=db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {request.email} already exists",
        )
    user = User(
        fname=request.fname,
        lname=request.lname,
        email=request.email,
        created_at=datetime.utcnow(),
        password=Hash.get_password_hash(request.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    pass


def update_user(id: int, request, db):
    user = get_user_by_id(id=id, db=db)
    user.fname = request.fname
    user.lname = request.lname
    user.email = request.email
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user
    pass


def delete_user(id: int, db):
    user = get_user_by_id(id=id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    db.delete(user)
    db.commit()
    return {
        "message": "User deleted successfully",
    }
    pass


def get_all_users(db):
    pass
