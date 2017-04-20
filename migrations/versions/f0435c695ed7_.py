"""empty message

Revision ID: f0435c695ed7
Revises: 7b02bd4ecf90
Create Date: 2017-04-19 19:06:29.266625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0435c695ed7'
down_revision = '7b02bd4ecf90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cape',
    sa.Column('subjectName', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('subjectName')
    )
    op.create_table('csec',
    sa.Column('subjectName', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('subjectName')
    )
    op.create_table('student',
    sa.Column('studentID', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('studentID')
    )
    op.create_table('application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('studentID', sa.String(length=50), nullable=True),
    sa.Column('subjectName', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['studentID'], ['student.studentID'], ),
    sa.ForeignKeyConstraint(['subjectName'], ['cape.subjectName'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('studied',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('studentID', sa.String(length=50), nullable=True),
    sa.Column('grade', sa.String(length=5), nullable=True),
    sa.Column('subjectName', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['studentID'], ['student.studentID'], ),
    sa.ForeignKeyConstraint(['subjectName'], ['csec.subjectName'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('studied')
    op.drop_table('application')
    op.drop_table('student')
    op.drop_table('csec')
    op.drop_table('cape')
    # ### end Alembic commands ###