"""seed_discount

Revision ID: 028008012afe
Revises: 12ad67f85c17
Create Date: 2025-04-08 19:55:58.068352

"""
import random
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '028008012afe'
down_revision: Union[str, None] = '12ad67f85c17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('UPDATE SALES SET DISCOUNT = round(random()::NUMERIC, 2)')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('UPDATE SALES SET DISCOUNT = NULL')
    # ### end Alembic commands ###
