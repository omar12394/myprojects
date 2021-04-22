"""empty message

Revision ID: 4f71968bcd22
Revises: 3b14fbd3c66f
Create Date: 2021-02-23 23:57:38.681203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f71968bcd22'
down_revision = '3b14fbd3c66f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.add_column('Shows', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.drop_constraint('Shows_artist_fkey', 'Shows', type_='foreignkey')
    op.drop_constraint('Shows_venue_fkey', 'Shows', type_='foreignkey')
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.drop_column('Shows', 'artist')
    op.drop_column('Shows', 'venue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('venue', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Shows', sa.Column('artist', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.create_foreign_key('Shows_venue_fkey', 'Shows', 'Venue', ['venue'], ['id'])
    op.create_foreign_key('Shows_artist_fkey', 'Shows', 'Artist', ['artist'], ['id'])
    op.drop_column('Shows', 'venue_id')
    op.drop_column('Shows', 'artist_id')
    # ### end Alembic commands ###