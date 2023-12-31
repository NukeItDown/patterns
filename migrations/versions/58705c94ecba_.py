"""empty message

Revision ID: 58705c94ecba
Revises: 85d15be3e70b
Create Date: 2023-12-14 22:59:30.665209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58705c94ecba'
down_revision = '85d15be3e70b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('similar_products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('identifynumber', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('similar_products', schema=None) as batch_op:
        batch_op.drop_column('identifynumber')

    # ### end Alembic commands ###
