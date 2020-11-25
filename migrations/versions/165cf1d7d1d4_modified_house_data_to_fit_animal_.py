"""Modified house data to fit animal health form.

Revision ID: 165cf1d7d1d4
Revises: 6400953a12df
Create Date: 2020-11-25 13:11:25.098171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '165cf1d7d1d4'
down_revision = '6400953a12df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('animal_health_house_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=20), nullable=False),
    sa.Column('farmer', sa.String(length=30), nullable=False),
    sa.Column('cattle_id', sa.String(length=20), nullable=False),
    sa.Column('cattle_name', sa.String(length=20), nullable=False),
    sa.Column('cattle_color', sa.String(length=10), nullable=False),
    sa.Column('cattle_sex', sa.String(), nullable=False),
    sa.Column('collar', sa.String(), nullable=True),
    sa.Column('pcv', sa.String(), nullable=True),
    sa.Column('diagnosis', sa.String(), nullable=True),
    sa.Column('treatment', sa.String(), nullable=True),
    sa.Column('cc_ml', sa.String(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_animal_health_house_data_code'), 'animal_health_house_data', ['code'], unique=True)
    op.drop_index('ix_housedata_code', table_name='housedata')
    op.drop_table('housedata')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('housedata',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('education', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('employment', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('marital_status', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('number_of_people', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('number_of_children', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('number_of_animals', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('economic_activity', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('type_of_animals', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('farming_activities', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('social_economic_data', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('code', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='housedata_user_id_fkey', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name='housedata_pkey')
    )
    op.create_index('ix_housedata_code', 'housedata', ['code'], unique=True)
    op.drop_index(op.f('ix_animal_health_house_data_code'), table_name='animal_health_house_data')
    op.drop_table('animal_health_house_data')
    # ### end Alembic commands ###