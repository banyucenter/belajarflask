"""hapus cascade

Revision ID: a764fff92405
Revises: 05f6770d0927
Create Date: 2021-01-07 22:09:56.369181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a764fff92405'
down_revision = '05f6770d0927'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('mahasiswa_ibfk_1', 'mahasiswa', type_='foreignkey')
    op.drop_constraint('mahasiswa_ibfk_2', 'mahasiswa', type_='foreignkey')
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_dua'], ['id'])
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_satu'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.create_foreign_key('mahasiswa_ibfk_2', 'mahasiswa', 'dosen', ['dosen_satu'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('mahasiswa_ibfk_1', 'mahasiswa', 'dosen', ['dosen_dua'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###