"""Added Security Model

Revision ID: c2210b4c2bdd
Revises: 02886a4afc2c
Create Date: 2019-12-14 14:49:33.283202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2210b4c2bdd'
down_revision = '02886a4afc2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('security_level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=65), nullable=True),
    sa.Column('name', sa.String(length=65), nullable=True),
    sa.Column('description', sa.String(length=65), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('sample', sa.Column('security_level', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'sample', 'security_level', ['security_level'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sample', type_='foreignkey')
    op.drop_column('sample', 'security_level')
    op.drop_table('security_level')
    # ### end Alembic commands ###
