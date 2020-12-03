"""Added weight field to housedata model

Revision ID: fa55d611d59d
Revises: 3f45c9122778
Create Date: 2020-12-02 09:40:45.507212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa55d611d59d'
down_revision = '3f45c9122778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animal_health_house_data', sa.Column('weight', sa.Float(precision=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('animal_health_house_data', 'weight')
    # ### end Alembic commands ###