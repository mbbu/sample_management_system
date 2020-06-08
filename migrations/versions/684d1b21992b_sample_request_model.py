"""Sample request model

Revision ID: 684d1b21992b
Revises: 795f01cfeab3
Create Date: 2020-06-08 11:04:34.657063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '684d1b21992b'
down_revision = '795f01cfeab3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('sample', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.DateTime(), nullable=False),
    sa.Column('response_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=25), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['sample'], ['sample.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sample_request')
    # ### end Alembic commands ###
