from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


# ---------------- USER ----------------

class UserCreate(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )


class UserResponse(BaseModel):

    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------- AUTH ----------------

class Token(BaseModel):

    access_token: str
    token_type: str


# ---------------- POSTS ----------------

class PostCreate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=200
    )

    content: str = Field(
        min_length=1
    )

    published: bool = True

    category_id: int | None = None

    tag_ids: list[int] = Field(
        default_factory=list
    )


class PostResponse(BaseModel):

    id: int
    title: str
    content: str
    published: bool
    author_id: int
    category_id: int | None

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------- CATEGORY ----------------

class CategoryCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=100
    )


class CategoryResponse(BaseModel):

    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------- TAG ----------------

class TagCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=50
    )


class TagResponse(BaseModel):

    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------- COMMENT ----------------

class CommentCreate(BaseModel):

    content: str = Field(
        min_length=1
    )


class CommentResponse(BaseModel):

    id: int
    content: str
    post_id: int
    author_id: int

    model_config = ConfigDict(
        from_attributes=True
    )