"""add reset_password feature for user

Revision ID: c223cce1a413
Revises: a143b60aad61
Create Date: 2018-08-23 11:57:25.950135

"""

# revision identifiers, used by Alembic.
revision = 'c223cce1a413'
down_revision = 'a143b60aad61'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('reset_password_token_created', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('reset_password_token_hash', sa.Unicode(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('reset_password_token_hash')
        batch_op.drop_column('reset_password_token_created')
    # ### end Alembic commands ###
