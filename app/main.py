from fastapi import (
    FastAPI,
    Depends,
    Request
)

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import (
    Jinja2Templates
)

from sqlalchemy.orm import Session

from .database import get_db

from . import models

from .models import (
    User,
    Post
)

from .dependencies import (
    get_current_user
)

from .routers import (
    auth,
    posts,
    categories,
    tags,
    comments,
    users
)


app = FastAPI(
    title="Blog API",
    version="1.0.0",
    description=(
        "A full-stack Blog API built "
        "with FastAPI and SQLAlchemy."
    )
)


app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)


templates = Jinja2Templates(
    directory="app/templates"
)


app.include_router(
    auth.router
)

app.include_router(
    posts.router
)

app.include_router(
    categories.router
)

app.include_router(
    tags.router
)

app.include_router(
    comments.router
)

app.include_router(
    users.router
)


@app.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request,
    db: Session = Depends(get_db)
):

    posts = db.query(Post).filter(
        Post.published == True
    ).all()


    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "posts": posts
        }
    )


@app.get(
    "/post/{post_id}",
    response_class=HTMLResponse
)
def post_detail(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(
        Post.id == post_id,
        Post.published == True
    ).first()


    if not post:

        return HTMLResponse(
            content="Post not found",
            status_code=404
        )


    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={
            "post": post
        }
    )


@app.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@app.get(
    "/post/{post_id}/edit",
    response_class=HTMLResponse
)
def edit_post_page(
    post_id: int,
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="edit_post.html",
        context={
            "post_id": post_id
        }
    )


@app.get(
    "/protected"
)
def protected_route(
    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "message":
            "You are authenticated",

        "username":
            current_user.username,

        "user_id":
            current_user.id
    }