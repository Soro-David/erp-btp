"""create chantiers, types, clients, responsables and documents tables

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-09-22 14:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Table chantier_types
    op.create_table(
        'chantier_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_chantier_types_id'), 'chantier_types', ['id'], unique=False)
    op.create_index(op.f('ix_chantier_types_name'), 'chantier_types', ['name'], unique=True)

    # 2. Table clients
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False, server_default='Particulier'),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('contact_person', sa.String(length=255), nullable=True),
        sa.Column('company_name', sa.String(length=255), nullable=True),
        sa.Column('rccm', sa.String(length=100), nullable=True),
        sa.Column('company_contact', sa.String(length=255), nullable=True),
        sa.Column('ministry', sa.String(length=255), nullable=True),
        sa.Column('direction', sa.String(length=255), nullable=True),
        sa.Column('service', sa.String(length=255), nullable=True),
        sa.Column('admin_in_charge', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)
    op.create_index(op.f('ix_clients_name'), 'clients', ['name'], unique=False)

    # 3. Table responsables
    op.create_table(
        'responsables',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('role_name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_responsables_id'), 'responsables', ['id'], unique=False)
    op.create_index(op.f('ix_responsables_role_name'), 'responsables', ['role_name'], unique=False)

    # 4. Table chantiers
    op.create_table(
        'chantiers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type_id', sa.Integer(), nullable=True),
        sa.Column('type_name', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='En préparation'),
        sa.Column('country', sa.String(length=100), nullable=False, server_default="Côte d'Ivoire"),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('commune', sa.String(length=100), nullable=True),
        sa.Column('district', sa.String(length=100), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('client_id', sa.Integer(), nullable=True),
        sa.Column('client_name', sa.String(length=255), nullable=True),
        sa.Column('project_manager_id', sa.Integer(), nullable=True),
        sa.Column('site_manager_id', sa.Integer(), nullable=True),
        sa.Column('foreman_id', sa.Integer(), nullable=True),
        sa.Column('hse_officer_id', sa.Integer(), nullable=True),
        sa.Column('design_office', sa.String(length=255), nullable=True),
        sa.Column('contractor', sa.String(length=255), nullable=True),
        sa.Column('start_date_planned', sa.Date(), nullable=False),
        sa.Column('end_date_planned', sa.Date(), nullable=False),
        sa.Column('estimated_duration_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('start_date_actual', sa.Date(), nullable=True),
        sa.Column('end_date_actual', sa.Date(), nullable=True),
        sa.Column('budget_estimated', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0.00'),
        sa.Column('cost_estimated', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0.00'),
        sa.Column('contract_amount', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0.00'),
        sa.Column('currency', sa.String(length=10), nullable=False, server_default='FCFA'),
        sa.Column('funding_mode', sa.String(length=100), nullable=True, server_default='Fonds propres'),
        sa.Column('surface_m2', sa.Float(), nullable=True),
        sa.Column('buildings_count', sa.Integer(), nullable=True),
        sa.Column('floors_count', sa.Integer(), nullable=True),
        sa.Column('soil_nature', sa.String(length=255), nullable=True),
        sa.Column('construction_method', sa.String(length=255), nullable=True),
        sa.Column('technical_description', sa.Text(), nullable=True),
        sa.Column('physical_progress', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('financial_progress', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('priority', sa.String(length=20), nullable=False, server_default='Normale'),
        sa.Column('observations', sa.Text(), nullable=True),
        sa.Column('is_draft', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['foreman_id'], ['responsables.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['hse_officer_id'], ['responsables.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['project_manager_id'], ['responsables.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['site_manager_id'], ['responsables.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['type_id'], ['chantier_types.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_chantiers_code'), 'chantiers', ['code'], unique=True)
    op.create_index(op.f('ix_chantiers_id'), 'chantiers', ['id'], unique=False)
    op.create_index(op.f('ix_chantiers_name'), 'chantiers', ['name'], unique=False)

    # 5. Table chantier_documents
    op.create_table(
        'chantier_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chantier_id', sa.Integer(), nullable=False),
        sa.Column('document_type', sa.String(length=100), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chantier_id'], ['chantiers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_chantier_documents_id'), 'chantier_documents', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('chantier_documents')
    op.drop_table('chantiers')
    op.drop_table('responsables')
    op.drop_table('clients')
    op.drop_table('chantier_types')
