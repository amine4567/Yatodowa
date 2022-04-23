"""initial migration

Revision ID: 462c50a875f1
Revises: 
Create Date: 2022-04-13 21:14:23.011995

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "462c50a875f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lists_groups",
        sa.Column("group_name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("group_name"),
    )
    op.create_table(
        "tasks_lists",
        sa.Column("list_name", sa.String(length=20), nullable=False),
        sa.Column("group_name", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ["group_name"],
            ["lists_groups.group_name"],
        ),
        sa.PrimaryKeyConstraint("list_name"),
    )
    op.create_table(
        "tasks",
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("text", sa.String(length=200), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=True),
        sa.Column("list_name", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["list_name"],
            ["tasks_lists.list_name"],
        ),
        sa.PrimaryKeyConstraint("task_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tasks")
    op.drop_table("tasks_lists")
    op.drop_table("lists_groups")
    # ### end Alembic commands ###
