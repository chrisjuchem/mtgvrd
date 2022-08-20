"""add draft options

Revision ID: 6f8487781c8b
Revises: 12fe4c066e38
Create Date: 2022-08-09 11:44:50.941152

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "6f8487781c8b"
down_revision = "12fe4c066e38"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade():
    op.add_column(
        "drafts",
        sa.Column("multiseat", sa.Boolean(), server_default="f", nullable=False),
    )
    op.add_column(
        "drafts",
        sa.Column("random_seats", sa.Boolean(), server_default="t", nullable=False),
    )


def downgrade():
    op.drop_column("drafts", "random_seats")
    op.drop_column("drafts", "multiseat")
