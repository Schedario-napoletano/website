"""add target_id

Revision ID: fc7e7e332052
Revises: ec5136ec9dab
Create Date: 2022-03-26 12:40:32.331997

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fc7e7e332052'
down_revision = 'ec5136ec9dab'
branch_labels = None
depends_on = None


def upgrade():
    # old column
    op.drop_column('definition', 'target')
    # new ones
    op.add_column('definition', sa.Column('target_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_definition_target_id'), 'definition', ['target_id'], unique=False)
    op.create_foreign_key(None, 'definition', 'definition', ['target_id'], ['id'])


def downgrade():
    # new column
    op.drop_constraint(None, 'definition', type_='foreignkey')
    op.drop_index(op.f('ix_definition_target_id'), table_name='definition')
    op.drop_column('definition', 'target_id')
    # old one
    op.add_column('definition', sa.Column('target', sa.VARCHAR(), autoincrement=False, nullable=True))
