from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'd243d06d597a'
down_revision = 'af17072e7522'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the desired schema
    op.create_table(
        'new_restaurants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(80), nullable=True),  # Remove NOT NULL constraint
        sa.Column('address', sa.String(200), nullable=False),
    )

    # Copy data from the old table to the new table
    op.execute('''
        INSERT INTO new_restaurants (id, name, address)
        SELECT id, name, address FROM restaurants
    ''')

    # Drop the old table
    op.drop_table('restaurants')

    # Rename the new table to the old table's name
    op.rename_table('new_restaurants', 'restaurants')

def downgrade():
    # Create the old table schema
    op.create_table(
        'new_restaurants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(80), nullable=False),
        sa.Column('address', sa.String(200), nullable=False),
    )

    # Copy data from the current table to the new table
    op.execute('''
        INSERT INTO new_restaurants (id, name, address)
        SELECT id, name, address FROM restaurants
    ''')

    # Drop the current table
    op.drop_table('restaurants')

    # Rename the new table to the old table's name
    op.rename_table('new_restaurants', 'restaurants')
