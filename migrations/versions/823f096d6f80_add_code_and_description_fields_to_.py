"""Add code and description fields to dynamic models

Revision ID: 823f096d6f80
Revises: e3a5f6e78096
Create Date: 2025-03-31 02:04:37.295063
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '823f096d6f80'
down_revision = 'e3a5f6e78096'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('building_code', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=20), nullable=False, server_default='UNKNOWN'))
        batch_op.add_column(sa.Column('description', sa.String(length=100), nullable=False, server_default='Geçici açıklama'))
        batch_op.create_unique_constraint('uq_building_code_code', ['code'])
        batch_op.drop_column('name')

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=20), nullable=False, server_default='UNKNOWN'))
        batch_op.add_column(sa.Column('description', sa.String(length=100), nullable=False, server_default='Geçici açıklama'))
        batch_op.create_unique_constraint('uq_category_code', ['code'])
        batch_op.drop_column('name')

    with op.batch_alter_table('discipline', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=20), nullable=False, server_default='UNKNOWN'))
        batch_op.add_column(sa.Column('description', sa.String(length=100), nullable=False, server_default='Geçici açıklama'))
        batch_op.create_unique_constraint('uq_discipline_code', ['code'])
        batch_op.drop_column('name')

    with op.batch_alter_table('document_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=20), nullable=False, server_default='UNKNOWN'))
        batch_op.add_column(sa.Column('description', sa.String(length=100), nullable=False, server_default='Geçici açıklama'))
        batch_op.create_unique_constraint('uq_document_type_code', ['code'])
        batch_op.drop_column('name')

    with op.batch_alter_table('originator', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=20), nullable=False, server_default='UNKNOWN'))
        batch_op.add_column(sa.Column('description', sa.String(length=100), nullable=False, server_default='Geçici açıklama'))
        batch_op.create_unique_constraint('uq_originator_code', ['code'])
        batch_op.drop_column('name')


def downgrade():
    with op.batch_alter_table('originator', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_originator_code', type_='unique')
        batch_op.drop_column('description')
        batch_op.drop_column('code')

    with op.batch_alter_table('document_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_document_type_code', type_='unique')
        batch_op.drop_column('description')
        batch_op.drop_column('code')

    with op.batch_alter_table('discipline', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_discipline_code', type_='unique')
        batch_op.drop_column('description')
        batch_op.drop_column('code')

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_category_code', type_='unique')
        batch_op.drop_column('description')
        batch_op.drop_column('code')

    with op.batch_alter_table('building_code', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_building_code_code', type_='unique')
        batch_op.drop_column('description')
        batch_op.drop_column('code')
