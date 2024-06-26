"""Added rating model and removed rating from recipe

Revision ID: dd5761f230f4
Revises: 318cb0943c6a
Create Date: 2024-03-27 09:03:41.328340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd5761f230f4'
down_revision = '318cb0943c6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('scent', sa.Float(), nullable=False),
    sa.Column('stability', sa.Float(), nullable=False),
    sa.Column('texture', sa.Float(), nullable=False),
    sa.Column('efficacy', sa.Float(), nullable=False),
    sa.Column('tolerance', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.INTEGER(), nullable=True))

    op.drop_table('rating')
    # ### end Alembic commands ###
