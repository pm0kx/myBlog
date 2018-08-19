"""Initial migration

Revision ID: 2dd682ea280d
Revises: d0d3041ada5a
Create Date: 2018-06-23 15:13:41.130193

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2dd682ea280d'
down_revision = 'd0d3041ada5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('action_log', 'modified_time')
    op.drop_column('action_log', 'creater')
    op.drop_column('action_log', 'modifier')
    op.drop_column('action_log', 'status')
    op.drop_column('action_log', 'created_time')
    op.drop_column('attach_resources', 'modified_time')
    op.drop_column('attach_resources', 'creater')
    op.drop_column('attach_resources', 'modifier')
    op.drop_column('attach_resources', 'status')
    op.drop_column('attach_resources', 'created_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attach_resources', sa.Column('created_time', mysql.DATETIME(), nullable=True))
    op.add_column('attach_resources', sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('attach_resources', sa.Column('modifier', mysql.VARCHAR(length=45), nullable=True))
    op.add_column('attach_resources', sa.Column('creater', mysql.VARCHAR(length=45), nullable=True))
    op.add_column('attach_resources', sa.Column('modified_time', mysql.DATETIME(), nullable=True))
    op.add_column('action_log', sa.Column('created_time', mysql.DATETIME(), nullable=True))
    op.add_column('action_log', sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('action_log', sa.Column('modifier', mysql.VARCHAR(length=45), nullable=True))
    op.add_column('action_log', sa.Column('creater', mysql.VARCHAR(length=45), nullable=True))
    op.add_column('action_log', sa.Column('modified_time', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###