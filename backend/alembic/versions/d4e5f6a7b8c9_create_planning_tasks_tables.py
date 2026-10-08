"""create planning, phases, tasks, subtasks, dependencies and milestones tables

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-09-22 18:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Table projects
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='En cours'),
        sa.Column('budget', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0.00'),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_projects_code'), 'projects', ['code'], unique=True)
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    op.create_index(op.f('ix_projects_name'), 'projects', ['name'], unique=False)

    # 2. Add project_id to chantiers
    op.add_column('chantiers', sa.Column('project_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_chantiers_project_id_projects',
        'chantiers', 'projects',
        ['project_id'], ['id'],
        ondelete='SET NULL'
    )

    # 3. Table phases (Lots / Phases de travaux)
    op.create_table(
        'phases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('chantier_id', sa.Integer(), nullable=False),
        sa.Column('responsible_id', sa.Integer(), nullable=True),
        sa.Column('start_date_planned', sa.Date(), nullable=True),
        sa.Column('end_date_planned', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='À faire'),
        sa.Column('progress', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chantier_id'], ['chantiers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['responsible_id'], ['responsables.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_phases_id'), 'phases', ['id'], unique=False)
    op.create_index(op.f('ix_phases_code'), 'phases', ['code'], unique=False)
    op.create_index(op.f('ix_phases_name'), 'phases', ['name'], unique=False)
    op.create_index(op.f('ix_phases_chantier_id'), 'phases', ['chantier_id'], unique=False)

    # 4. Table tasks (Tâches et sous-tâches)
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('chantier_id', sa.Integer(), nullable=False),
        sa.Column('phase_id', sa.Integer(), nullable=False),
        sa.Column('parent_task_id', sa.Integer(), nullable=True),
        sa.Column('responsible_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='À faire'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='Normale'),
        sa.Column('progress', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('weight', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('planned_start_date', sa.Date(), nullable=False),
        sa.Column('planned_end_date', sa.Date(), nullable=False),
        sa.Column('estimated_duration_days', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('actual_start_date', sa.Date(), nullable=True),
        sa.Column('actual_end_date', sa.Date(), nullable=True),
        sa.Column('delay_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_blocked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('blocking_reason', sa.String(length=255), nullable=True),
        sa.Column('blocking_date', sa.Date(), nullable=True),
        sa.Column('blocking_comment', sa.Text(), nullable=True),
        sa.Column('blocking_impact', sa.String(length=255), nullable=True),
        sa.Column('team_name', sa.String(length=100), nullable=True),
        sa.Column('workers_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('equipment', sa.Text(), nullable=True),
        sa.Column('materials', sa.Text(), nullable=True),
        sa.Column('budget_estimated', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0.00'),
        sa.Column('actual_cost', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0.00'),
        sa.Column('observations', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chantier_id'], ['chantiers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['phase_id'], ['phases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['responsible_id'], ['responsables.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_code'), 'tasks', ['code'], unique=True)
    op.create_index(op.f('ix_tasks_name'), 'tasks', ['name'], unique=False)
    op.create_index(op.f('ix_tasks_chantier_id'), 'tasks', ['chantier_id'], unique=False)
    op.create_index(op.f('ix_tasks_phase_id'), 'tasks', ['phase_id'], unique=False)
    op.create_index(op.f('ix_tasks_parent_task_id'), 'tasks', ['parent_task_id'], unique=False)

    # 5. Table task_dependencies
    op.create_table(
        'task_dependencies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('predecessor_id', sa.Integer(), nullable=False),
        sa.Column('successor_id', sa.Integer(), nullable=False),
        sa.Column('dependency_type', sa.String(length=50), nullable=False, server_default='FINISH_TO_START'),
        sa.Column('lag_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['predecessor_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['successor_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.CheckConstraint('predecessor_id != successor_id', name='check_no_self_dependency'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_task_dependencies_id'), 'task_dependencies', ['id'], unique=False)
    op.create_index(op.f('ix_task_dependencies_predecessor_id'), 'task_dependencies', ['predecessor_id'], unique=False)
    op.create_index(op.f('ix_task_dependencies_successor_id'), 'task_dependencies', ['successor_id'], unique=False)

    # 6. Table milestones
    op.create_table(
        'milestones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('chantier_id', sa.Integer(), nullable=False),
        sa.Column('responsible_id', sa.Integer(), nullable=True),
        sa.Column('planned_date', sa.Date(), nullable=False),
        sa.Column('actual_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='À venir'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chantier_id'], ['chantiers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['responsible_id'], ['responsables.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_milestones_id'), 'milestones', ['id'], unique=False)
    op.create_index(op.f('ix_milestones_code'), 'milestones', ['code'], unique=False)
    op.create_index(op.f('ix_milestones_chantier_id'), 'milestones', ['chantier_id'], unique=False)

    # 7. Table task_histories
    op.create_table(
        'task_histories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('field_name', sa.String(length=100), nullable=False),
        sa.Column('old_value', sa.Text(), nullable=True),
        sa.Column('new_value', sa.Text(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_task_histories_id'), 'task_histories', ['id'], unique=False)
    op.create_index(op.f('ix_task_histories_task_id'), 'task_histories', ['task_id'], unique=False)


def downgrade() -> None:
    op.drop_table('task_histories')
    op.drop_table('milestones')
    op.drop_table('task_dependencies')
    op.drop_table('tasks')
    op.drop_table('phases')
    op.drop_constraint('fk_chantiers_project_id_projects', 'chantiers', type_='foreignkey')
    op.drop_column('chantiers', 'project_id')
    op.drop_table('projects')
