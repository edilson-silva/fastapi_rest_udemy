"""Init

Revision ID: 4767f89e9cec
Revises: 
Create Date: 2022-04-24 15:33:01.564240

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4767f89e9cec"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "books",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("author", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="books_pkey"),
    )
    op.create_index("ix_books_id", "books", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_books_id", table_name="books")
    op.drop_table("books")
    # ### end Alembic commands ###
