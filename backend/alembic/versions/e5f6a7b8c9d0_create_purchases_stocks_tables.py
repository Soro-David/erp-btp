"""create purchases, suppliers, materials, stocks, movements, inventories and purchase documents tables

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-09-23 21:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5f6a7b8c9d0'
down_revision: Union[str, None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Table suppliers
    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('trade_name', sa.String(length=255), nullable=True),
        sa.Column('contact_name', sa.String(length=150), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), server_default='Abidjan', nullable=True),
        sa.Column('country', sa.String(length=100), server_default="Côte d'Ivoire", nullable=False),
        sa.Column('rccm', sa.String(length=100), nullable=True),
        sa.Column('ncc', sa.String(length=100), nullable=True),
        sa.Column('payment_terms', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_suppliers_id'), 'suppliers', ['id'], unique=False)
    op.create_index(op.f('ix_suppliers_code'), 'suppliers', ['code'], unique=True)
    op.create_index(op.f('ix_suppliers_name'), 'suppliers', ['name'], unique=False)

    # 2. Table material_categories
    op.create_table(
        'material_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_material_categories_id'), 'material_categories', ['id'], unique=False)
    op.create_index(op.f('ix_material_categories_code'), 'material_categories', ['code'], unique=True)
    op.create_index(op.f('ix_material_categories_name'), 'material_categories', ['name'], unique=True)

    # 3. Table material_units
    op.create_table(
        'material_units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_material_units_id'), 'material_units', ['id'], unique=False)
    op.create_index(op.f('ix_material_units_code'), 'material_units', ['code'], unique=True)

    # 4. Table materials
    op.create_table(
        'materials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('unit_id', sa.Integer(), nullable=False),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('indicative_price', sa.Numeric(precision=15, scale=2), server_default='0.00', nullable=True),
        sa.Column('minimum_stock', sa.Float(), server_default='0', nullable=False),
        sa.Column('maximum_stock', sa.Float(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['category_id'], ['material_categories.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['unit_id'], ['material_units.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_materials_id'), 'materials', ['id'], unique=False)
    op.create_index(op.f('ix_materials_code'), 'materials', ['code'], unique=True)
    op.create_index(op.f('ix_materials_name'), 'materials', ['name'], unique=False)

    # 5. Table stock_locations
    op.create_table(
        'stock_locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('type', sa.String(length=50), server_default='Dépôt principal', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_stock_locations_id'), 'stock_locations', ['id'], unique=False)
    op.create_index(op.f('ix_stock_locations_code'), 'stock_locations', ['code'], unique=True)
    op.create_index(op.f('ix_stock_locations_name'), 'stock_locations', ['name'], unique=False)

    # 6. Table purchases
    op.create_table(
        'purchases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reference', sa.String(length=50), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('chantier_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='Brouillon', nullable=False),
        sa.Column('payment_status', sa.String(length=50), server_default='Non payé', nullable=False),
        sa.Column('payment_mode', sa.String(length=50), server_default='Virement', nullable=True),
        sa.Column('subject', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('total_amount', sa.Numeric(precision=15, scale=2), server_default='0.00', nullable=False),
        sa.Column('currency', sa.String(length=10), server_default='FCFA', nullable=False),
        sa.Column('is_quick_purchase', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['chantier_id'], ['chantiers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_purchases_id'), 'purchases', ['id'], unique=False)
    op.create_index(op.f('ix_purchases_reference'), 'purchases', ['reference'], unique=True)
    op.create_index(op.f('ix_purchases_supplier_id'), 'purchases', ['supplier_id'], unique=False)
    op.create_index(op.f('ix_purchases_chantier_id'), 'purchases', ['chantier_id'], unique=False)
    op.create_index(op.f('ix_purchases_task_id'), 'purchases', ['task_id'], unique=False)

    # 7. Table purchase_lines
    op.create_table(
        'purchase_lines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('material_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('quantity_received', sa.Float(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['material_id'], ['materials.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_purchase_lines_id'), 'purchase_lines', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_lines_purchase_id'), 'purchase_lines', ['purchase_id'], unique=False)
    op.create_index(op.f('ix_purchase_lines_material_id'), 'purchase_lines', ['material_id'], unique=False)

    # 8. Table purchase_receipts
    op.create_table(
        'purchase_receipts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('receipt_number', sa.String(length=50), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['location_id'], ['stock_locations.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_purchase_receipts_id'), 'purchase_receipts', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_receipts_receipt_number'), 'purchase_receipts', ['receipt_number'], unique=True)
    op.create_index(op.f('ix_purchase_receipts_purchase_id'), 'purchase_receipts', ['purchase_id'], unique=False)

    # 9. Table purchase_receipt_items
    op.create_table(
        'purchase_receipt_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('receipt_id', sa.Integer(), nullable=False),
        sa.Column('purchase_line_id', sa.Integer(), nullable=False),
        sa.Column('material_id', sa.Integer(), nullable=False),
        sa.Column('quantity_received', sa.Float(), nullable=False),
        sa.Column('quantity_rejected', sa.Float(), server_default='0', nullable=False),
        sa.Column('rejection_reason', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['receipt_id'], ['purchase_receipts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['purchase_line_id'], ['purchase_lines.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['material_id'], ['materials.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_purchase_receipt_items_id'), 'purchase_receipt_items', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_receipt_items_receipt_id'), 'purchase_receipt_items', ['receipt_id'], unique=False)

    # 10. Table stock_movements
    op.create_table(
        'stock_movements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reference', sa.String(length=50), nullable=False),
        sa.Column('material_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('movement_type', sa.String(length=50), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=15, scale=2), server_default='0.00', nullable=True),
        sa.Column('chantier_id', sa.Integer(), nullable=True),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('purchase_id', sa.Integer(), nullable=True),
        sa.Column('source_location_id', sa.Integer(), nullable=True),
        sa.Column('dest_location_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['material_id'], ['materials.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['location_id'], ['stock_locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['chantier_id'], ['chantiers.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['source_location_id'], ['stock_locations.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['dest_location_id'], ['stock_locations.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_stock_movements_id'), 'stock_movements', ['id'], unique=False)
    op.create_index(op.f('ix_stock_movements_reference'), 'stock_movements', ['reference'], unique=True)
    op.create_index(op.f('ix_stock_movements_material_id'), 'stock_movements', ['material_id'], unique=False)
    op.create_index(op.f('ix_stock_movements_location_id'), 'stock_movements', ['location_id'], unique=False)
    op.create_index(op.f('ix_stock_movements_chantier_id'), 'stock_movements', ['chantier_id'], unique=False)
    op.create_index(op.f('ix_stock_movements_movement_type'), 'stock_movements', ['movement_type'], unique=False)

    # 11. Table stock_inventories
    op.create_table(
        'stock_inventories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reference', sa.String(length=50), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('inventory_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='Brouillon', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['location_id'], ['stock_locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_stock_inventories_id'), 'stock_inventories', ['id'], unique=False)
    op.create_index(op.f('ix_stock_inventories_reference'), 'stock_inventories', ['reference'], unique=True)

    # 12. Table stock_inventory_items
    op.create_table(
        'stock_inventory_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('inventory_id', sa.Integer(), nullable=False),
        sa.Column('material_id', sa.Integer(), nullable=False),
        sa.Column('theoretical_quantity', sa.Float(), server_default='0', nullable=False),
        sa.Column('actual_quantity', sa.Float(), server_default='0', nullable=False),
        sa.Column('discrepancy', sa.Float(), server_default='0', nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=15, scale=2), server_default='0.00', nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['inventory_id'], ['stock_inventories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['material_id'], ['materials.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_stock_inventory_items_id'), 'stock_inventory_items', ['id'], unique=False)
    op.create_index(op.f('ix_stock_inventory_items_inventory_id'), 'stock_inventory_items', ['inventory_id'], unique=False)

    # 13. Table purchase_documents
    op.create_table(
        'purchase_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('document_type', sa.String(length=100), nullable=False),
        sa.Column('document_number', sa.String(length=100), nullable=True),
        sa.Column('document_date', sa.Date(), nullable=True),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('file_size', sa.Integer(), server_default='0', nullable=False),
        sa.Column('uploaded_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_purchase_documents_id'), 'purchase_documents', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_documents_purchase_id'), 'purchase_documents', ['purchase_id'], unique=False)


def downgrade() -> None:
    op.drop_table('purchase_documents')
    op.drop_table('stock_inventory_items')
    op.drop_table('stock_inventories')
    op.drop_table('stock_movements')
    op.drop_table('purchase_receipt_items')
    op.drop_table('purchase_receipts')
    op.drop_table('purchase_lines')
    op.drop_table('purchases')
    op.drop_table('stock_locations')
    op.drop_table('materials')
    op.drop_table('material_units')
    op.drop_table('material_categories')
    op.drop_table('suppliers')
