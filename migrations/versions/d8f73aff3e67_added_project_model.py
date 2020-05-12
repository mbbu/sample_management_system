"""Added project model

Revision ID: d8f73aff3e67
Revises: 71d15bad42b6
Create Date: 2020-05-12 10:40:58.493911

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd8f73aff3e67'
down_revision = '71d15bad42b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(length=20), nullable=False),
                    sa.Column('theme_id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['theme_id'], ['theme.id'], ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_project_code'), 'project', ['code'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_code'), table_name='project')
    op.drop_table('project')
    # ### end Alembic commands ###
