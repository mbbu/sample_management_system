"""Number of tray not unique but code is

Revision ID: 73f9752b5d49
Revises: a3d3444cccde
Create Date: 2020-12-08 14:37:46.812583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73f9752b5d49'
down_revision = 'a3d3444cccde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('animal_health_house_data', 'weight',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    op.drop_constraint('tray_number_key', 'tray', type_='unique')
    op.create_unique_constraint(None, 'tray', ['code'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tray', type_='unique')
    op.create_unique_constraint('tray_number_key', 'tray', ['number'])
    op.alter_column('animal_health_house_data', 'weight',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    # ### end Alembic commands ###
