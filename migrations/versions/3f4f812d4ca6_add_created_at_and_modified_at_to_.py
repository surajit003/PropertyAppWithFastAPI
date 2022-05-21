"""add created_at and modified_at to message table

Revision ID: 3f4f812d4ca6
Revises: 913be17e323f
Create Date: 2022-05-21 14:55:23.504250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f4f812d4ca6'
down_revision = '913be17e323f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('message', sa.Column('modified_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'modified_at')
    op.drop_column('message', 'created_at')
    # ### end Alembic commands ###
