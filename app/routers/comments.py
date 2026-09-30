from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import (
    Comment,
    Post,
    User
)

from ..schemas import (
    CommentCreate,
    CommentResponse
)

from ..dependencies import (
    get_current_user,
    get_current_admin
)


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/{post_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
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


    comment = Comment(
        content=comment_data.content,
        post_id=post_id,
        author_id=current_user.id
    )


    db.add(comment)
    db.commit()
    db.refresh(comment)


    return comment


@router.get(
    "/post/{post_id}",
    response_model=list[CommentResponse]
)
def get_post_comments(
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


    return db.query(Comment).filter(
        Comment.post_id == post_id
    ).all()


@router.delete(
    "/admin/{comment_id}"
)
def admin_delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()


    if not comment:

        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )


    db.delete(comment)
    db.commit()


    return {
        "message":
            "Comment deleted by admin"
    }


@router.delete(
    "/{comment_id}"
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()


    if not comment:

        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )


    if (
        comment.author_id != current_user.id
        and not current_user.is_admin
    ):

        raise HTTPException(
            status_code=403,
            detail=(
                "You are not allowed "
                "to delete this comment"
            )
        )


    db.delete(comment)
    db.commit()


    return {
        "message":
            "Comment deleted successfully"
    }