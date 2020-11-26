"""Added study block to models.

Revision ID: 40f6db64fc74
Revises: c1be6963f46d
Create Date: 2020-11-26 10:10:06.825710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40f6db64fc74'
down_revision = 'c1be6963f46d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('study_block',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('area', sa.String(length=65), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=65), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('area')
    )
    op.create_index(op.f('ix_study_block_code'), 'study_block', ['code'], unique=True)
    op.create_index(op.f('ix_study_block_name'), 'study_block', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_study_block_name'), table_name='study_block')
    op.drop_index(op.f('ix_study_block_code'), table_name='study_block')
    op.drop_table('study_block')
    # ### end Alembic commands ###
