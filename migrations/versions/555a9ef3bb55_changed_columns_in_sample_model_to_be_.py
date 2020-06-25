"""Changed Columns in Sample Model to be nullable

Revision ID: 555a9ef3bb55
Revises: 335e9050c869
Create Date: 2019-12-11 16:13:37.751023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '555a9ef3bb55'
down_revision = '335e9050c869'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_table('sampletest')
    op.alter_column('sample', 'amount',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('sample', 'location_collected',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('sample', 'project',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('sample', 'project_owner',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('sample', 'sample_description',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('sample', 'sample_type',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('sample', 'temperature',
               existing_type=sa.NUMERIC(precision=5, scale=2),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sample', 'temperature',
               existing_type=sa.NUMERIC(precision=5, scale=2),
               nullable=False)
    op.alter_column('sample', 'sample_type',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('sample', 'sample_description',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.alter_column('sample', 'project_owner',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('sample', 'project',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.alter_column('sample', 'location_collected',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('sample', 'amount',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
