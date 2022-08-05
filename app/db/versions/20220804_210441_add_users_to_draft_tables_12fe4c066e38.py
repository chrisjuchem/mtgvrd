"""add users to draft tables

Revision ID: 12fe4c066e38
Revises: 514d4ee6a636
Create Date: 2022-08-04 21:04:41.970619

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "12fe4c066e38"
down_revision = "514d4ee6a636"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade():
    # If you have added a new table and it does not show up, make sure you
    # have added it to db/models/__init__.py
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("drafts", sa.Column("created_ts", sa.DateTime(), nullable=True))
    op.add_column("drafts", sa.Column("owner_id", postgresql.UUID(), nullable=True))
    op.alter_column(
        "drafts",
        "format",
        existing_type=postgresql.ENUM("VRD", name="format"),
        server_default="VRD",
        existing_nullable=False,
    )
    op.alter_column(
        "drafts",
        "pick_order",
        existing_type=postgresql.ENUM("snake", name="pick_order"),
        server_default="snake",
        existing_nullable=False,
    )
    op.alter_column(
        "drafts",
        "picks_made",
        existing_type=sa.INTEGER(),
        server_default="0",
        existing_nullable=False,
    )
    op.create_foreign_key(None, "drafts", "users", ["owner_id"], ["id"])
    op.add_column("seats", sa.Column("player_id", postgresql.UUID(), nullable=True))
    op.add_column("seats", sa.Column("joined_ts", sa.DateTime(), nullable=True))
    op.create_foreign_key(None, "seats", "users", ["player_id"], ["id"])
    op.alter_column("users", "discord_id", existing_type=sa.VARCHAR(length=24), nullable=True)
    op.alter_column("users", "last_login", existing_type=postgresql.TIMESTAMP(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "last_login", existing_type=postgresql.TIMESTAMP(), nullable=False)
    op.alter_column("users", "discord_id", existing_type=sa.VARCHAR(length=24), nullable=False)
    op.drop_column("seats", "joined_ts")
    op.drop_column("seats", "player_id")
    op.alter_column(
        "drafts",
        "picks_made",
        existing_type=sa.INTEGER(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "drafts",
        "pick_order",
        existing_type=postgresql.ENUM("snake", name="pick_order"),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "drafts",
        "format",
        existing_type=postgresql.ENUM("VRD", name="format"),
        server_default=None,
        existing_nullable=False,
    )
    op.drop_column("drafts", "owner_id")
    op.drop_column("drafts", "created_ts")
    # ### end Alembic commands ###