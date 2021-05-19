"""first

Revision ID: 0260305c5a46
Revises: 
Create Date: 2021-05-19 21:50:36.422152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0260305c5a46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipment_model',
    sa.Column('uid', sa.CHAR(32), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('equipment',
    sa.Column('uid', sa.CHAR(32), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('model', sa.CHAR(32), nullable=True),
    sa.Column('status', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['model'], ['equipment_model.uid'], name='fk_equipment_equipment_model_uid_model'),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipment')
    op.drop_table('equipment_model')
    # ### end Alembic commands ###