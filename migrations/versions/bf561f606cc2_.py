"""empty message

Revision ID: bf561f606cc2
Revises: 
Create Date: 2021-06-07 22:44:45.956130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf561f606cc2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cuisines',
    sa.Column('cuisine_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cuisine_name', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('cuisine_id')
    )
    op.create_table('ingredients',
    sa.Column('ing_id', sa.String(length=64), nullable=False),
    sa.Column('ing_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('ing_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('lists',
    sa.Column('list_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('list_name', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('list_id')
    )
    op.create_table('recipes',
    sa.Column('recipe_id', sa.String(length=64), nullable=False),
    sa.Column('recipe_name', sa.String(length=200), nullable=True),
    sa.Column('img_url', sa.String(length=10000), nullable=True),
    sa.Column('instructions', sa.String(length=10000), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    op.create_table('bookmarks',
    sa.Column('bookmark_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('recipe_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('bookmark_id')
    )
    op.create_table('list_ingredients',
    sa.Column('l_i_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('list_id', sa.Integer(), nullable=True),
    sa.Column('ing_id', sa.String(length=64), nullable=True),
    sa.Column('meas_unit', sa.String(length=30), nullable=True),
    sa.Column('mass_qty', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ing_id'], ['ingredients.ing_id'], ),
    sa.ForeignKeyConstraint(['list_id'], ['lists.list_id'], ),
    sa.PrimaryKeyConstraint('l_i_id')
    )
    op.create_table('recipe_cuisines',
    sa.Column('recipe_cuisine_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cuisine_id', sa.Integer(), nullable=True),
    sa.Column('recipe_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['cuisine_id'], ['cuisines.cuisine_id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('recipe_cuisine_id')
    )
    op.create_table('recipe_ingredients',
    sa.Column('r_i_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('recipe_id', sa.String(length=64), nullable=True),
    sa.Column('ing_id', sa.String(length=64), nullable=True),
    sa.Column('meas_unit', sa.String(length=30), nullable=True),
    sa.Column('mass_qty', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ing_id'], ['ingredients.ing_id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('r_i_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_ingredients')
    op.drop_table('recipe_cuisines')
    op.drop_table('list_ingredients')
    op.drop_table('bookmarks')
    op.drop_table('recipes')
    op.drop_table('lists')
    op.drop_table('followers')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('ingredients')
    op.drop_table('cuisines')
    # ### end Alembic commands ###
