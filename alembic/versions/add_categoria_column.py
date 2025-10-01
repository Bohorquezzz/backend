"""add categoria column to reto table

Revision ID: add_categoria_column
Revises: 
Create Date: 2025-10-01

"""
from alembic import op
import sqlalchemy as sa
from app.models.database import RetoCategoria

# revision identifiers, used by Alembic.
revision = 'add_categoria_column'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create enum type first
    categoria_enum = sa.Enum('SOCIAL', 'FISICA', 'INTELECTUAL', name='retocategoria')
    categoria_enum.create(op.get_bind(), checkfirst=True)

    # Add the categoria column
    op.add_column('reto',
        sa.Column('categoria', 
                  sa.Enum('SOCIAL', 'FISICA', 'INTELECTUAL', name='retocategoria'),
                  nullable=False,
                  server_default='SOCIAL')
    )

def downgrade():
    # Remove the categoria column
    op.drop_column('reto', 'categoria')
    
    # Drop the enum type
    categoria_enum = sa.Enum(name='retocategoria')
    categoria_enum.drop(op.get_bind())