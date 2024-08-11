"""create post table

Revision ID: 252da4a518d0
Revises: 
Create Date: 2024-08-10 18:18:09.227360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '252da4a518d0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("postsa", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("content", sa.String(), nullable=False),
                    sa.Column("published", sa.Boolean(),
                              nullable=False, server_default='True'),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    )
    pass


def downgrade() -> None:
    op.drop_table("postsa")
    pass
