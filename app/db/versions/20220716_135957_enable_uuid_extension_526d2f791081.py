"""enable uuid extension

Revision ID: 526d2f791081
Revises:
Create Date: 2022-07-16 13:59:57.722064

"""
from alembic.op import execute

# revision identifiers, used by Alembic.
revision = "526d2f791081"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    execute('create extension "uuid-ossp"')


def downgrade():
    execute('drop extension "uuid-ossp"')
