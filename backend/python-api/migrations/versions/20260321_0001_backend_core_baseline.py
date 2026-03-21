"""backend core baseline

Revision ID: 20260321_0001
Revises:
Create Date: 2026-03-21 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260321_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "notification_preferences",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("list_change_push_enabled", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_notification_preferences_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", name="pk_notification_preferences"),
    )

    op.create_table(
        "auth_identities",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("provider_subject", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_auth_identities_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_auth_identities"),
        sa.UniqueConstraint("provider", "provider_subject", name="uq_auth_identities_provider_subject"),
    )

    op.create_table(
        "device_push_tokens",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("platform", sa.String(length=20), nullable=False),
        sa.Column("push_token", sa.String(length=255), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_device_push_tokens_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_device_push_tokens"),
    )

    op.create_table(
        "list_snapshots",
        sa.Column("list_id", sa.String(), nullable=False),
        sa.Column("snapshot_type", sa.String(length=30), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_by_user_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], name="fk_list_snapshots_created_by_user_id_users", ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name="pk_list_snapshots"),
    )

    op.create_table(
        "shopping_lists",
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("owner_user_id", sa.String(), nullable=False),
        sa.Column("last_active_item_snapshot_id", sa.String(), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["last_active_item_snapshot_id"], ["list_snapshots.id"], name="fk_shopping_lists_last_active_item_snapshot_id_list_snapshots", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"], name="fk_shopping_lists_owner_user_id_users", ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name="pk_shopping_lists"),
    )

    op.create_table(
        "list_memberships",
        sa.Column("list_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["list_id"], ["shopping_lists.id"], name="fk_list_memberships_list_id_shopping_lists", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_list_memberships_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_list_memberships"),
        sa.UniqueConstraint("list_id", "user_id", name="uq_list_memberships_list_id_user_id"),
    )

    op.create_table(
        "list_items",
        sa.Column("list_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("unit", sa.String(length=30), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("is_purchased", sa.Boolean(), nullable=False),
        sa.Column("is_template_item", sa.Boolean(), nullable=False),
        sa.Column("sort_index", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by_user_id", sa.String(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["list_id"], ["shopping_lists.id"], name="fk_list_items_list_id_shopping_lists", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"], name="fk_list_items_updated_by_user_id_users", ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name="pk_list_items"),
    )

    op.create_table(
        "realtime_events",
        sa.Column("list_id", sa.String(), nullable=False),
        sa.Column("event_type", sa.String(length=60), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["list_id"], ["shopping_lists.id"], name="fk_realtime_events_list_id_shopping_lists", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_realtime_events"),
    )

    op.create_table(
        "share_links",
        sa.Column("list_id", sa.String(), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_user_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], name="fk_share_links_created_by_user_id_users", ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["list_id"], ["shopping_lists.id"], name="fk_share_links_list_id_shopping_lists", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_share_links"),
        sa.UniqueConstraint("token_hash", name="uq_share_links_token_hash"),
    )


def downgrade() -> None:
    op.drop_table("share_links")
    op.drop_table("realtime_events")
    op.drop_table("list_items")
    op.drop_table("list_memberships")
    op.drop_table("shopping_lists")
    op.drop_table("list_snapshots")
    op.drop_table("device_push_tokens")
    op.drop_table("auth_identities")
    op.drop_table("notification_preferences")
    op.drop_table("users")
