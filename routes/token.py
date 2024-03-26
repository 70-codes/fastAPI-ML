from . import create_route
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from repository import auth_repo
from fastapi.security import OAuth2PasswordRequestForm

router = create_route(
    prefix="login",
    tags="Authentication",
)


@router.post("")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return auth_repo.get_user_by_email(
        request=request,
        db=db,
    )
    pass
