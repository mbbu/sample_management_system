"""Updates on sample projoject_fk

Revision ID: 3a78e1d46857
Revises: 44fdc8ab8e6a
Create Date: 2021-01-27 17:36:16.169581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a78e1d46857'
down_revision = '44fdc8ab8e6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('animal_health_house_data', 'weight',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    op.alter_column('sample', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sample', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('animal_health_house_data', 'weight',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    # ### end Alembic commands ###
