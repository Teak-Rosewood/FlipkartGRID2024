"""Initializing DB

Revision ID: eab98d9323bb
Revises: 
Create Date: 2024-12-11 17:50:05.233280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eab98d9323bb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scan_db',
    sa.Column('scan_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('processed', sa.Boolean(), nullable=True),
    sa.Column('items_detected', sa.JSON(), nullable=True),
    sa.Column('item_summary', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('scan_id')
    )
    op.create_index(op.f('ix_scan_db_scan_id'), 'scan_db', ['scan_id'], unique=False)
    op.create_table('fres_db',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('scan_id', sa.Integer(), nullable=False),
    sa.Column('produce', sa.String(), nullable=True),
    sa.Column('freshness', sa.Integer(), nullable=True),
    sa.Column('shelf_life', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['scan_id'], ['scan_db.scan_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id', 'scan_id', name='fesh_db_pk')
    )
    op.create_index(op.f('ix_fres_db_shelf_life'), 'fres_db', ['shelf_life'], unique=False)
    op.create_table('image_db',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('scan_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('ocr_text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['scan_id'], ['scan_db.scan_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('image_id', 'scan_id', name='iamge_db_pk')
    )
    op.create_table('product_db',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('scan_id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('expiry_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('expired', sa.Boolean(), nullable=True),
    sa.Column('shelf_life', sa.Integer(), nullable=True),
    sa.Column('summary', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['scan_id'], ['scan_db.scan_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id', 'scan_id')
    )
    op.create_index(op.f('ix_product_db_shelf_life'), 'product_db', ['shelf_life'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_db_shelf_life'), table_name='product_db')
    op.drop_table('product_db')
    op.drop_table('image_db')
    op.drop_index(op.f('ix_fres_db_shelf_life'), table_name='fres_db')
    op.drop_table('fres_db')
    op.drop_index(op.f('ix_scan_db_scan_id'), table_name='scan_db')
    op.drop_table('scan_db')
    # ### end Alembic commands ###
