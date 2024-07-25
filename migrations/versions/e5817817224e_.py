from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e5817817224e'
down_revision = 'd243d06d597a'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the updated schema
    op.create_table(
        'restaurants_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('address', sa.String(length=200), nullable=False),
    )

    # Copy data from the old table to the new table
    op.execute("""
        INSERT INTO restaurants_new (id, name, address)
        SELECT id, name, address FROM restaurants
    """)

    # Drop the old table
    op.drop_table('restaurants')

    # Rename the new table to the original table name
    op.rename_table('restaurants_new', 'restaurants')


def downgrade():
    # Create a new table with the old schema
    op.create_table(
        'restaurants_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=80), nullable=True),  # Old schema had nullable name
        sa.Column('address', sa.String(length=200), nullable=False),
    )

    # Copy data from the current table to the old table
    op.execute("""
        INSERT INTO restaurants_old (id, name, address)
        SELECT id, name, address FROM restaurants
    """)

    # Drop the current table
    op.drop_table('restaurants')

    # Rename the old table to the original table name
    op.rename_table('restaurants_old', 'restaurants')
