"""add moodle sessions

Revision ID: a6b33037e05a
Revises: 05c4dd22a80f
Create Date: 2021-09-15 22:31:51.939339

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a6b33037e05a"
down_revision = "05c4dd22a80f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "moodlebot_moodle_sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("telegram_user_id", sa.Integer(), nullable=True),
        sa.Column("hash", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["telegram_user_id"],
            ["moodlebot_telegram_users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("moodlebot_moodle_sessions")
    # ### end Alembic commands ###
