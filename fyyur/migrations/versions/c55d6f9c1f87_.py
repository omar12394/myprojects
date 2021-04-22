"""empty message

Revision ID: c55d6f9c1f87
Revises: 
Create Date: 2021-02-23 00:57:51.778205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c55d6f9c1f87'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    op.add_column('Artist', sa.Column('seeking', sa.Boolean(), nullable=True))
    op.drop_column('Artist', 'seaking')
    op.add_column('Shows', sa.Column('start_time', sa.Date(), nullable=True))
    op.add_column('Venue', sa.Column('past_shows', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    op.create_foreign_key(None, 'Venue', 'Shows', ['past_shows'], ['id'])
    op.drop_column('Venue', 'seaking')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seaking', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'past_shows')
    op.drop_column('Shows', 'start_time')
    op.add_column('Artist', sa.Column('seaking', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking')
    op.create_table('person',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='person_pkey')
    )
    # ### end Alembic commands ###
