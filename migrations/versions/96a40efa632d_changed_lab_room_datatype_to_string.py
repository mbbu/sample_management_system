"""Changed lab room datatype to string

Revision ID: 96a40efa632d
Revises: c54130e1a1f1
Create Date: 2020-02-21 11:39:06.645819

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '96a40efa632d'
down_revision = 'c54130e1a1f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(u'lab_code', 'laboratory', ['code'])
    op.alter_column('laboratory', 'room', existing_type=sa.Integer(), type_=sa.String())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'lab_code', 'laboratory', type_='unique')
    op.alter_column('laboratory', 'room', existing_type=sa.String(), type_=sa.Integer())
    # ### end Alembic commands ###
