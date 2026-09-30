from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import (
    Post,
    User,
    Category,
    Tag
)

from ..schemas import (
    PostCreate,
    PostResponse
)

from ..dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


def validate_category_and_tags(
    post_data: PostCreate,
    db: Session
):

    if post_data.category_id:

        category = db.query(Category).filter(
            Category.id == post_data.category_id
        ).first()


        if not category:

            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )


    tags = []


    if post_data.tag_ids:

        unique_tag_ids = set(
            post_data.tag_ids
        )


        tags = db.query(Tag).filter(
            Tag.id.in_(unique_tag_ids)
        ).all()


        if len(tags) != len(unique_tag_ids):

            raise HTTPException(
                status_code=404,
                detail="One or more tags not found"
            )


    return tags


@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    tags = validate_category_and_tags(
        post_data,
        db
    )


    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        published=post_data.published,
        author_id=current_user.id,
        category_id=post_data.category_id,
        tags=tags
    )


    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post


@router.get(
    "/my",
    response_model=list[PostResponse]
)
def get_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return db.query(Post).filter(
        Post.author_id == current_user.id
    ).all()


@router.get(
    "/",
    response_model=list[PostResponse]
)
def get_posts(
    page: int = Query(
        1,
        ge=1
    ),

    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    search: str | None = None,

    category_id: int | None = None,

    db: Session = Depends(get_db)
):

    query = db.query(Post).filter(
        Post.published == True
    )


    if search:

        search_pattern = f"%{search}%"


        query = query.filter(
            (
                Post.title.ilike(
                    search_pattern
                )
            )
            |
            (
                Post.content.ilike(
                    search_pattern
                )
            )
        )


    if category_id:

        query = query.filter(
            Post.category_id == category_id
        )


    offset = (
        page - 1
    ) * limit


    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get(
    "/my/{post_id}",
    response_model=PostResponse
)
def get_my_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    post = db.query(Post).filter(
        Post.id == post_id,
        Post.author_id == current_user.id
    ).first()


    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    return post


@router.get(
    "/{post_id}",
    response_model=PostResponse
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(
        Post.id == post_id,
        Post.published == True
    ).first()


    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    return post


@router.put(
    "/{post_id}",
    response_model=PostResponse
)
def update_post(
    post_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()


    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    if post.author_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail=(
                "You are not allowed "
                "to update this post"
            )
        )


    tags = validate_category_and_tags(
        post_data,
        db
    )


    post.title = post_data.title
    post.content = post_data.content
    post.published = post_data.published
    post.category_id = post_data.category_id
    post.tags = tags


    db.commit()
    db.refresh(post)


    return post


@router.delete(
    "/{post_id}"
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()


    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    if (
        post.author_id != current_user.id
        and not current_user.is_admin
    ):

        raise HTTPException(
            status_code=403,
            detail=(
                "You are not allowed "
                "to delete this post"
            )
        )


    db.delete(post)
    db.commit()


    return {
        "message":
            "Post deleted successfully"
    }