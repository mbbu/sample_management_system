"""Change location_collected type from string to JSON

Revision ID: 2573c8070e75
Revises: 797dc311403e
Create Date: 2020-06-17 10:30:29.225255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2573c8070e75'
down_revision = '797dc311403e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sample', 'location_collected',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.JSON(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sample', 'location_collected',
               existing_type=sa.JSON(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###