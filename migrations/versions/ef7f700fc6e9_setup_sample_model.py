"""Setup Sample Model

Revision ID: ef7f700fc6e9
Revises: 54af49545db8
Create Date: 2019-11-13 12:52:50.301399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef7f700fc6e9'
down_revision = '54af49545db8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('animal_species', sa.String(length=100), nullable=False),
    sa.Column('sample_type', sa.String(length=100), nullable=False),
    sa.Column('sample_description', sa.String(length=150), nullable=False),
    sa.Column('location_collected', sa.String(length=100), nullable=False),
    sa.Column('project', sa.String(length=150), nullable=False),
    sa.Column('project_owner', sa.String(length=100), nullable=False),
    sa.Column('retension_period', sa.Integer(), nullable=True),
    sa.Column('barcode', sa.String(length=100), nullable=False),
    sa.Column('analysis', sa.String(length=100), nullable=True),
    sa.Column('temperature_level', sa.String(length=100), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sample')
    # ### end Alembic commands ###
