"""adding try user table

Revision ID: e39e8bd14f3e
Revises: 64f44097c172
Create Date: 2024-07-16 11:04:43.723306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e39e8bd14f3e'
down_revision: Union[str, None] = '64f44097c172'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category_table',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=255), nullable=True),
    sa.Column('category_description', sa.String(length=255), nullable=True),
    sa.Column('category_count', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.String(length=255), nullable=True),
    sa.Column('edited_date', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_index(op.f('ix_category_table_category_name'), 'category_table', ['category_name'], unique=False)
    op.create_table('subcategory_table',
    sa.Column('subcategory_id', sa.Integer(), nullable=False),
    sa.Column('subcategory_name', sa.String(length=255), nullable=True),
    sa.Column('subcategory_description', sa.String(length=255), nullable=True),
    sa.Column('subcategory_count', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.String(length=255), nullable=True),
    sa.Column('edited_date', sa.String(length=255), nullable=True),
    sa.Column('subcategory_category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subcategory_category_id'], ['category_table.category_id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('subcategory_id')
    )
    op.create_index(op.f('ix_subcategory_table_subcategory_name'), 'subcategory_table', ['subcategory_name'], unique=False)
    op.create_table('product_table',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=True),
    sa.Column('product_description', sa.String(length=255), nullable=True),
    sa.Column('product_price', sa.Integer(), nullable=True),
    sa.Column('product_quantity', sa.Integer(), nullable=True),
    sa.Column('product_image_name', sa.String(length=255), nullable=False),
    sa.Column('product_image_path', sa.String(length=255), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.String(length=255), nullable=True),
    sa.Column('edited_date', sa.String(length=255), nullable=True),
    sa.Column('product_category_id', sa.Integer(), nullable=False),
    sa.Column('product_subcategory_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_category_id'], ['category_table.category_id'], onupdate='CASCADE'),
    sa.ForeignKeyConstraint(['product_subcategory_id'], ['subcategory_table.subcategory_id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_index(op.f('ix_product_table_product_name'), 'product_table', ['product_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_table_product_name'), table_name='product_table')
    op.drop_table('product_table')
    op.drop_index(op.f('ix_subcategory_table_subcategory_name'), table_name='subcategory_table')
    op.drop_table('subcategory_table')
    op.drop_index(op.f('ix_category_table_category_name'), table_name='category_table')
    op.drop_table('category_table')
    # ### end Alembic commands ###
