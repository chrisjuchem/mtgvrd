"""add draft tables

Revision ID: 917327be5b47
Revises: d4a308b9cee2
Create Date: 2022-07-27 16:59:37.828914

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision = "917327be5b47"
down_revision = "d4a308b9cee2"
branch_labels = None
depends_on = None
# pylint: enable=invalid-name


def upgrade():
    # If you have added a new table and it does not show up, make sure you
    # have added it to db/models/__init__.py
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "drafts",
        sa.Column(
            "id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False
        ),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("start_ts", sa.DateTime(), nullable=True),
        sa.Column("format", sa.Enum("VRD", name="format"), nullable=False),
        sa.Column("n_seats", sa.Integer(), nullable=False),
        sa.Column("pick_order", sa.Enum("snake", name="pick_order"), nullable=False),
        sa.Column("rounds", sa.Integer(), nullable=False),
        sa.Column("picks_made", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "seats",
        sa.Column(
            "id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False
        ),
        sa.Column("draft_id", postgresql.UUID(), nullable=False),
        sa.Column("seat_no", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["draft_id"], ["drafts.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("draft_id", "seat_no"),
    )
    op.create_table(
        "picks",
        sa.Column("draft_id", postgresql.UUID(), nullable=False),
        sa.Column("seat_id", postgresql.UUID(), nullable=False),
        sa.Column("pick_no", sa.Integer(), nullable=False),
        sa.Column("round", sa.Integer(), nullable=False),
        sa.Column("card_id", postgresql.UUID(), nullable=False),
        sa.Column("pick_ts", sa.DateTime(), nullable=True),
        sa.Column("finalized_ts", sa.DateTime(), nullable=True),
        sa.Column("maindeck", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["card_id"],
            ["cards.oracle_id"],
        ),
        sa.ForeignKeyConstraint(["draft_id"], ["drafts.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["seat_id"], ["seats.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("draft_id", "pick_no"),
    )
    op.create_index("seat_idx", "picks", ["seat_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("seat_idx", table_name="picks")
    op.drop_table("picks")
    op.drop_table("seats")
    op.drop_table("drafts")
    op.execute("DROP TYPE format;")
    op.execute("DROP TYPE pick_order;")
    # ### end Alembic commands ###
