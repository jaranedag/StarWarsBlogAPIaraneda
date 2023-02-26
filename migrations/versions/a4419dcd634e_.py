"""empty message

Revision ID: a4419dcd634e
Revises: 2a54382eb54f
Create Date: 2023-02-22 18:55:37.836846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4419dcd634e'
down_revision = '2a54382eb54f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('fav__people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_name', sa.String(length=120), nullable=True),
    sa.Column('user_fav', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['people_name'], ['people.name'], ),
    sa.ForeignKeyConstraint(['user_fav'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fav__people')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###