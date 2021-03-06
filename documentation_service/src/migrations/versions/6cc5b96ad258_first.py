"""first

Revision ID: 6cc5b96ad258
Revises: 
Create Date: 2021-05-10 14:14:34.023581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cc5b96ad258'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('file_uid', sa.CHAR(32), nullable=False),
    sa.Column('file_name', sa.String(length=50), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=False),
    sa.Column('equipment_model_uid', sa.CHAR(32), nullable=False),
    sa.PrimaryKeyConstraint('file_uid'),
    sa.UniqueConstraint('file_name'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents')
    # ### end Alembic commands ###
