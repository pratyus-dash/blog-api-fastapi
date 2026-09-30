from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import (
    UserCreate,
    UserResponse,
    Token
)

from ..auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()


    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(
            user_data.password
        )
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


@router.post(
    "/token",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )


    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }