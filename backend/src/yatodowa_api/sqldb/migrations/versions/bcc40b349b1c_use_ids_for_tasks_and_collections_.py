"""use ids for tasks and collections foreign keys instead of names

Revision ID: bcc40b349b1c
Revises: 68a0c99af01e
Create Date: 2022-04-24 17:05:41.823657

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "bcc40b349b1c"
down_revision = "68a0c99af01e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "collections",
        sa.Column("group_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.drop_constraint("collections_group_name_fkey", "collections", type_="foreignkey")
    op.create_foreign_key(None, "collections", "groups", ["group_id"], ["group_id"])
    op.drop_column("collections", "group_name")
    op.add_column(
        "tasks",
        sa.Column("collection_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.drop_constraint("tasks_collection_name_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(
        None, "tasks", "collections", ["collection_id"], ["collection_id"]
    )
    op.drop_column("tasks", "collection_name")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tasks",
        sa.Column(
            "collection_name",
            sa.VARCHAR(length=20),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_collection_name_fkey",
        "tasks",
        "collections",
        ["collection_name"],
        ["name"],
    )
    op.drop_column("tasks", "collection_id")
    op.add_column(
        "collections",
        sa.Column(
            "group_name", sa.VARCHAR(length=20), autoincrement=False, nullable=True
        ),
    )
    op.drop_constraint(None, "collections", type_="foreignkey")
    op.create_foreign_key(
        "collections_group_name_fkey", "collections", "groups", ["group_name"], ["name"]
    )
    op.drop_column("collections", "group_id")
    # ### end Alembic commands ###
