"""changed subcategory and product table

Revision ID: 0bf736308efd
Revises: 03fac0ff9119
Create Date: 2024-07-23 18:49:01.329866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bf736308efd'
down_revision: Union[str, None] = '03fac0ff9119'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_table', sa.Column('try_column', sa.String(length=255), nullable=True))
    op.add_column('subcategory_table', sa.Column('try_column', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subcategory_table', 'try_column')
    op.drop_column('product_table', 'try_column')
    # ### end Alembic commands ###
