from . import create_route
from schemas import CreateUser, CreateUserAsAdmin, ShowUser, UpdateUser
from fastapi import status, Depends
from database import get_db
from sqlalchemy.orm import Session
from repository import user_repo
from typing import List
from authentication import get_current_user

router = create_route(
    "user",
    "User",
)


# @router.get("/", response_model=List[ShowUser])
# async def get_all_users(db: Session = Depends(get_db)):
#     return user_repo.get_all_users(db=db)
#     pass


@router.post(
    "/",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: CreateUser,
    db: Session = Depends(get_db),
):
    return user_repo.create_user(
        request=request,
        db=db,
    )
    pass


@router.get("/{id}", response_model=ShowUser)
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    user: CreateUser = Depends(get_current_user),
):
    return user_repo.get_user_by_id(id=id, db=db)
    pass


@router.patch("/")
async def update_user(
    id: int,
    request: UpdateUser,
    db: Session = Depends(get_db),
    user: CreateUser = Depends(get_current_user),
):
    return user_repo.update_user(
        id=id,
        request=request,
        db=db,
    )
    pass


@router.delete("/{id}")
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    user: CreateUser = Depends(get_current_user),
):
    return user_repo.delete_user(id=id, db=db)
    pass
