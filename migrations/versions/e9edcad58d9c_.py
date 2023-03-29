"""empty message

Revision ID: e9edcad58d9c
Revises: c332b632d603
Create Date: 2023-03-29 00:58:49.387803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9edcad58d9c'
down_revision = 'c332b632d603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=13), nullable=False))
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(length=6), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('age')
        batch_op.drop_column('phone')

    # ### end Alembic commands ###