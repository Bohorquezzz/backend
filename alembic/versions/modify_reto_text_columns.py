"""modify reto text columns

Revision ID: modify_reto_text_columns
Revises: 13da8fe234e3
Create Date: 2025-10-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'modify_reto_text_columns'
down_revision = '13da8fe234e3'
branch_labels = None
depends_on = None

def upgrade():
    # Modificar la columna nombre_reto a LONGTEXT
    op.alter_column('reto', 'nombre_reto',
        existing_type=mysql.VARCHAR(length=50),
        type_=mysql.LONGTEXT,
        existing_nullable=True)
    
    # Modificar la columna descripcion_reto a LONGTEXT
    op.alter_column('reto', 'descripcion_reto',
        existing_type=mysql.VARCHAR(length=50),
        type_=mysql.LONGTEXT,
        existing_nullable=True)

def downgrade():
    # Revertir la columna descripcion_reto a VARCHAR(50)
    op.alter_column('reto', 'descripcion_reto',
        existing_type=mysql.LONGTEXT,
        type_=mysql.VARCHAR(length=50),
        existing_nullable=True)
    
    # Revertir la columna nombre_reto a VARCHAR(50)
    op.alter_column('reto', 'nombre_reto',
        existing_type=mysql.LONGTEXT,
        type_=mysql.VARCHAR(length=50),
        existing_nullable=True)