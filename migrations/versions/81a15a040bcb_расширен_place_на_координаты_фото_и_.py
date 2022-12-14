"""расширен place на координаты фото и адрес

Revision ID: 81a15a040bcb
Revises: 7e7b28b54f9e
Create Date: 2022-11-16 10:33:39.197661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81a15a040bcb'
down_revision = '7e7b28b54f9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('place_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('places', sa.Column('lat', sa.Float(), nullable=True))
    op.add_column('places', sa.Column('lng', sa.Float(), nullable=True))
    op.add_column('places', sa.Column('address', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('places', 'address')
    op.drop_column('places', 'lng')
    op.drop_column('places', 'lat')
    op.drop_table('place_photos')
    # ### end Alembic commands ###
