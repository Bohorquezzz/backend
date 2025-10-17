"""modify reto columns to TEXT type

Revision ID: 20251016_modify_reto_text
Revises: 13da8fe234e3
Create Date: 2025-10-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '20251016_modify_reto_text'
down_revision = '13da8fe234e3'
branch_labels = None
depends_on = None

def upgrade():
    # Modificar las columnas a TEXT
    op.execute('ALTER TABLE reto MODIFY COLUMN nombre_reto TEXT;')
    op.execute('ALTER TABLE reto MODIFY COLUMN descripcion_reto TEXT;')

def downgrade():
    # Revertir las columnas a VARCHAR(50)
    op.execute('ALTER TABLE reto MODIFY COLUMN nombre_reto VARCHAR(50);')
    op.execute('ALTER TABLE reto MODIFY COLUMN descripcion_reto VARCHAR(50);')