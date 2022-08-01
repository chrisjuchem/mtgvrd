"""add_users

Revision ID: 514d4ee6a636
Revises: 917327be5b47
Create Date: 2022-07-28 15:48:11.423110

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "514d4ee6a636"
down_revision = "917327be5b47"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade():
    op.create_table(
        "users",
        sa.Column(
            "id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False
        ),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("discord_id", sa.String(length=24), nullable=False),
        sa.Column("last_login", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("discord_idx", "users", ["discord_id"], unique=True)


def downgrade():
    op.drop_index("discord_idx", table_name="users")
    op.drop_table("users")
