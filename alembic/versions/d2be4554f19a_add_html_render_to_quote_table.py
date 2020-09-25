"""add html_render to quote table

Revision ID: d2be4554f19a
Revises: 
Create Date: 2020-09-25 18:44:43.349661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2be4554f19a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("quote", sa.Column("html_render", sa.String, server_default=""))


def downgrade():
    op.drop_column("quote", "html_render")
