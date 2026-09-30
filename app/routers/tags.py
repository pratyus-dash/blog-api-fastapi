from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Tag
from ..schemas import TagCreate, TagResponse


router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED
)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db)
):
    existing_tag = db.query(Tag).filter(
        Tag.name == tag_data.name
    ).first()

    if existing_tag:
        raise HTTPException(
            status_code=400,
            detail="Tag already exists"
        )

    tag = Tag(
        name=tag_data.name
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


@router.get(
    "/",
    response_model=list[TagResponse]
)
def get_tags(
    db: Session = Depends(get_db)
):
    return db.query(Tag).all()