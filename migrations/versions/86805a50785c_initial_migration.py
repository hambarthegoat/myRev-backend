"""Initial migration

Revision ID: 86805a50785c
Revises:
Create Date: 2026-06-05 16:45:24.420469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86805a50785c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'sales',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tanggal', sa.Date(), nullable=False),
        sa.Column('bulan', sa.Integer(), nullable=False),
        sa.Column('nama_item', sa.String(length=255), nullable=False),
        sa.Column('kategori', sa.String(length=50), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('harga_satuan', sa.Integer(), nullable=False),
        sa.Column('total_harga', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sales')
