"""create cards

Revision ID: d4a308b9cee2
Revises: 526d2f791081
Create Date: 2022-07-19 17:21:44.177661

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "d4a308b9cee2"
down_revision = "526d2f791081"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade():
    op.create_table(
        "cards",
        sa.Column("oracle_id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_uri", sa.String(), nullable=False),
        sa.Column("vrd_legal", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("oracle_id"),
    )


def downgrade():
    op.drop_table("cards")
