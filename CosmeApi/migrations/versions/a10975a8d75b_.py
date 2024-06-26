"""empty message

Revision ID: a10975a8d75b
Revises: 
Create Date: 2024-03-02 12:41:59.031611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a10975a8d75b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('CAS', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('INCI_name', sa.String(length=100), nullable=False),
    sa.Column('function', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('ph_min', sa.Float(), nullable=True),
    sa.Column('ph_max', sa.Float(), nullable=True),
    sa.Column('temp_min', sa.Float(), nullable=True),
    sa.Column('temp_max', sa.Float(), nullable=True),
    sa.Column('use_level_min', sa.Float(), nullable=True),
    sa.Column('use_level_max', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('CAS')
    )
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('instructions', sa.Text(), nullable=True),
    sa.Column('version_of', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('order_number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe_ingredient_phase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('phase_id', sa.Integer(), nullable=False),
    sa.Column('CAS', sa.String(length=100), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['CAS'], ['ingredient.CAS'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['phase_id'], ['phase.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_ingredient_phase')
    op.drop_table('phase')
    op.drop_table('recipe')
    op.drop_table('ingredient')
    # ### end Alembic commands ###
