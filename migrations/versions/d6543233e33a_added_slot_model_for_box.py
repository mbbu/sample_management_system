"""Added slot model for box

Revision ID: d6543233e33a
Revises: 5ff467f2f7d5
Create Date: 2020-09-28 11:40:52.088017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6543233e33a'
down_revision = '5ff467f2f7d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('slot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('box_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=65), nullable=False),
    sa.Column('position', sa.JSON(), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['box_id'], ['box.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_slot_code'), 'slot', ['code'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_slot_code'), table_name='slot')
    op.drop_table('slot')
    # ### end Alembic commands ###
