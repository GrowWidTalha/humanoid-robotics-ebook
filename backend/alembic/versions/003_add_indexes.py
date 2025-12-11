"""Add database indexes for performance

Revision ID: 003
Revises: 002
Create Date: 2025-12-06

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Indexes for chat_messages table
    op.create_index(
        'idx_chat_messages_user_id',
        'chat_messages',
        ['user_id']
    )

    op.create_index(
        'idx_chat_messages_thread_id',
        'chat_messages',
        ['thread_id']
    )

    op.create_index(
        'idx_chat_messages_created_at',
        'chat_messages',
        ['created_at'],
        postgresql_using='btree',
        postgresql_ops={'created_at': 'DESC'}
    )

    # Indexes for sessions table
    op.create_index(
        'idx_sessions_user_id',
        'sessions',
        ['user_id']
    )

    op.create_index(
        'idx_sessions_expires_at',
        'sessions',
        ['expires_at']
    )


def downgrade() -> None:
    # Drop sessions indexes
    op.drop_index('idx_sessions_expires_at')
    op.drop_index('idx_sessions_user_id')

    # Drop chat_messages indexes
    op.drop_index('idx_chat_messages_created_at')
    op.drop_index('idx_chat_messages_thread_id')
    op.drop_index('idx_chat_messages_user_id')
