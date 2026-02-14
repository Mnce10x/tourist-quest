"""initial

Revision ID: 0001
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('documents', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('source_url', sa.String(length=1024)), sa.Column('object_key', sa.String(length=255)), sa.Column('file_hash', sa.String(length=64)), sa.Column('content_type', sa.String(length=64)), sa.Column('created_at', sa.DateTime()))
    op.create_table('kpi_records', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('report_id', sa.String(length=100)), sa.Column('report_period', sa.String(length=32)), sa.Column('publish_date', sa.Date()), sa.Column('programme', sa.String(length=255)), sa.Column('kpi_name', sa.String(length=255)), sa.Column('kpi_target', sa.String(length=100)), sa.Column('kpi_actual', sa.String(length=100)), sa.Column('variance', sa.Float()), sa.Column('variance_reason', sa.Text()), sa.Column('audit_flag', sa.Boolean()), sa.Column('evidence', sa.JSON()))
    op.create_table('expenditure_records', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('report_id', sa.String(length=100)), sa.Column('expenditure_vote', sa.String(length=100)), sa.Column('programme', sa.String(length=255)), sa.Column('item', sa.String(length=255)), sa.Column('planned_budget', sa.Float()), sa.Column('actual_spend', sa.Float()), sa.Column('variance', sa.Float()), sa.Column('variance_reason', sa.Text()), sa.Column('procurement_notes', sa.Text()), sa.Column('evidence', sa.JSON()))
    op.create_table('media_records', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('media_id', sa.String(length=100)), sa.Column('source', sa.String(length=255)), sa.Column('date', sa.Date()), sa.Column('author', sa.String(length=255)), sa.Column('title', sa.String(length=500)), sa.Column('body_text', sa.Text()), sa.Column('entities', sa.JSON()), sa.Column('topics', sa.JSON()), sa.Column('sentiment_score', sa.Float()), sa.Column('stance', sa.String(length=32)), sa.Column('key_claims', sa.JSON()), sa.Column('risk_flags', sa.JSON()), sa.Column('evidence', sa.JSON()))
    op.create_table('recommendations', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('topic', sa.String(length=100)), sa.Column('action', sa.Text()), sa.Column('confidence', sa.Float()), sa.Column('rationale', sa.Text()), sa.Column('evidence', sa.JSON()))


def downgrade() -> None:
    op.drop_table('recommendations')
    op.drop_table('media_records')
    op.drop_table('expenditure_records')
    op.drop_table('kpi_records')
    op.drop_table('documents')
