"""Added code to box

Revision ID: 5801c9720bb1
Revises: f5aff887f40a
Create Date: 2020-02-13 09:34:48.283152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5801c9720bb1'
down_revision = 'f5aff887f40a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('box', sa.Column('code', sa.String(length=65), nullable=False))
    op.create_index(op.f('ix_box_code'), 'box', ['code'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_box_code'), table_name='box')
    op.drop_column('box', 'code')
    # ### end Alembic commands ###
