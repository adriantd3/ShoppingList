"""task 9 share links audit

Revision ID: 20260321_0003
Revises: 20260321_0002
Create Date: 2026-03-21 13:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260321_0003"
down_revision: Union[str, Sequence[str], None] = "20260321_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("share_links", sa.Column("revoked_by_user_id", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_share_links_revoked_by_user_id_users",
        "share_links",
        "users",
        ["revoked_by_user_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_share_links_revoked_by_user_id_users", "share_links", type_="foreignkey")
    op.drop_column("share_links", "revoked_by_user_id")
