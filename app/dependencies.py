from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .auth_utils import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )


    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        user_id = payload.get("sub")


        if user_id is None:

            raise credentials_exception


        user_id = int(user_id)


    except (
        JWTError,
        ValueError,
        TypeError
    ):

        raise credentials_exception


    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if user is None:

        raise credentials_exception


    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )


    return user


def get_current_admin(
    current_user: User = Depends(
        get_current_user
    )
):

    if not current_user.is_admin:

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


    return current_user