"""initial blog schema

Revision ID: 078574144134
Revises:
Create Date: 2026-09-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "078574144134"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all blog application tables."""

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "username",
            sa.String(length=50),
            nullable=False
        ),
        sa.Column(
            "email",
            sa.String(length=100),
            nullable=False
        ),
        sa.Column(
            "hashed_password",
            sa.String(length=255),
            nullable=False
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True
        ),
        sa.Column(
            "is_admin",
            sa.Boolean(),
            nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email")
    )

    op.create_index(
        "ix_users_id",
        "users",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_users_username",
        "users",
        ["username"],
        unique=True
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True
    )

    op.create_table(
        "categories",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name")
    )

    op.create_index(
        "ix_categories_id",
        "categories",
        ["id"],
        unique=False
    )

    op.create_table(
        "tags",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "name",
            sa.String(length=50),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name")
    )

    op.create_index(
        "ix_tags_id",
        "tags",
        ["id"],
        unique=False
    )

    op.create_table(
        "posts",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "title",
            sa.String(length=200),
            nullable=False
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False
        ),
        sa.Column(
            "published",
            sa.Boolean(),
            nullable=True
        ),
        sa.Column(
            "author_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "category_id",
            sa.Integer(),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"]
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_posts_id",
        "posts",
        ["id"],
        unique=False
    )

    op.create_table(
        "post_tags",
        sa.Column(
            "post_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "tag_id",
            sa.Integer(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"]
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"]
        ),
        sa.PrimaryKeyConstraint(
            "post_id",
            "tag_id"
        )
    )

    op.create_table(
        "comments",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False
        ),
        sa.Column(
            "post_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "author_id",
            sa.Integer(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"]
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_comments_id",
        "comments",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    """Drop all blog application tables."""

    op.drop_index(
        "ix_comments_id",
        table_name="comments"
    )
    op.drop_table("comments")

    op.drop_table("post_tags")

    op.drop_index(
        "ix_posts_id",
        table_name="posts"
    )
    op.drop_table("posts")

    op.drop_index(
        "ix_tags_id",
        table_name="tags"
    )
    op.drop_table("tags")

    op.drop_index(
        "ix_categories_id",
        table_name="categories"
    )
    op.drop_table("categories")

    op.drop_index(
        "ix_users_email",
        table_name="users"
    )
    op.drop_index(
        "ix_users_username",
        table_name="users"
    )
    op.drop_index(
        "ix_users_id",
        table_name="users"
    )
    op.drop_table("users")