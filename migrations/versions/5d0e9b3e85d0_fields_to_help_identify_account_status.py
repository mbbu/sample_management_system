"""Fields to help identify account status

Revision ID: 5d0e9b3e85d0
Revises: 12ddc471a96d
Create Date: 2020-05-06 10:42:59.461473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d0e9b3e85d0'
down_revision = '12ddc471a96d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email_confirmation_sent_on', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('email_confirmed', sa.Boolean(), nullable=False, server_default='false'))

    # help to fix errors on existing data in db
    # op.execute("UPDATE users SET email_confirmed = false ")
    # op.alter_column('users', email_confirmed, nullable=False)

    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='false'))
    # help to fix errors on existing data in db
    # op.execute("UPDATE users SET is_active = false ")
    # op.alter_column('users', is_active, nullable=False)

    op.add_column('users', sa.Column('email_confirmed_on', sa.DateTime(), nullable=True))

    op.drop_constraint('users_housedata_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'housedata_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('housedata_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_housedata_id_fkey', 'users', 'housedata', ['housedata_id'], ['id'], ondelete='SET NULL')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'email_confirmed_on')
    op.drop_column('users', 'email_confirmed')
    op.drop_column('users', 'email_confirmation_sent_on')
    # ### end Alembic commands ###
