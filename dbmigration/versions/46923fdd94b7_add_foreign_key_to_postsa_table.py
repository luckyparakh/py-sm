"""Add foreign key to postsa table

Revision ID: 46923fdd94b7
Revises: 976667f2b593
Create Date: 2024-08-10 18:49:57.304354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46923fdd94b7'
down_revision: Union[str, None] = '976667f2b593'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("postsa", sa.Column(
        "user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_user_fk", source_table="postsa",
                          referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_user_fk", "postsa", type_="foreignkey")
    op.drop_column("postsa", "user_id")
    pass
