"""init

Revision ID: 81d2dd9fee9e
Revises: 
Create Date: 2025-03-04 19:13:45.123424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81d2dd9fee9e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_category_id'], ['product_categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('shipping_methods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('addresses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('unit_number', sa.String(), nullable=False),
    sa.Column('street_number', sa.String(), nullable=False),
    sa.Column('address_line1', sa.String(), nullable=False),
    sa.Column('address_line2', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('region', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.Column('country_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('product_image', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['product_categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('variations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['product_categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('address_user',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('address_id', sa.UUID(), nullable=False),
    sa.Column('is_default', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'address_id')
    )
    op.create_table('orders',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('order_date', sa.Date(), nullable=False),
    sa.Column('shipping_address_id', sa.UUID(), nullable=False),
    sa.Column('shipping_method_id', sa.Integer(), nullable=False),
    sa.Column('order_total', sa.Numeric(), nullable=False),
    sa.Column('order_status_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_status_id'], ['order_statuses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['shipping_address_id'], ['addresses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['shipping_method_id'], ['shipping_methods.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_items',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('SKU', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('quantity_in_stock', sa.Integer(), nullable=False),
    sa.Column('product_image', sa.String(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shopping_carts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('variation_options',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('variation_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['variation_id'], ['variations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configuration_product',
    sa.Column('product_item_id', sa.UUID(), nullable=False),
    sa.Column('variation_option_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['product_item_id'], ['product_items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['variation_option_id'], ['variation_options.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_item_id', 'variation_option_id')
    )
    op.create_table('order_lines',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('product_item_id', sa.UUID(), nullable=False),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_item_id'], ['product_items.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shopping_cart_items',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('cart_id', sa.UUID(), nullable=False),
    sa.Column('product_item_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['shopping_carts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_item_id'], ['product_items.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shopping_cart_items')
    op.drop_table('order_lines')
    op.drop_table('configuration_product')
    op.drop_table('variation_options')
    op.drop_table('shopping_carts')
    op.drop_table('product_items')
    op.drop_table('orders')
    op.drop_table('address_user')
    op.drop_table('variations')
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('addresses')
    op.drop_table('shipping_methods')
    op.drop_table('roles')
    op.drop_table('product_categories')
    op.drop_table('order_statuses')
    op.drop_table('countries')
    # ### end Alembic commands ###
