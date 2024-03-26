from fastapi import HTTPException, status
from authentication.hash import Hash
from models import User
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from schemas import Token, TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0.5


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    pass


def get_user_by_email(request, db):
    """Get user by email Where the email
    that is in the database is being
    refered as the username from the request"""

    user = db.query(User).filter(User.email == request.username.lower()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong credentials",
        )
    if not Hash.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong credentials",
        )
    # Generate a JWT token and return it
    access_token = create_access_token(data={"sub": user.email, "id": user.id})
    return Token(access_token=access_token, token_type="bearer")
    pass
