"""Add categoria column to reto table

Revision ID: add_categoria_to_reto
"""
from alembic import op
import sqlalchemy as sa
from app.models.database import RetoCategoria

# revision identifiers, used by Alembic.
revision = 'add_categoria_to_reto'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add categoria column with a default value of 'SOCIAL'
    op.add_column('reto', sa.Column('categoria', 
                                  sa.Enum(RetoCategoria),
                                  server_default=RetoCategoria.SOCIAL.value,
                                  nullable=False))

def downgrade():
    # Remove the categoria column
    op.drop_column('reto', 'categoria')