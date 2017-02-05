"""empty message

Revision ID: 89028ebc40d1
Revises: 465785295fcb
Create Date: 2017-01-31 16:01:04.425086

"""

# revision identifiers, used by Alembic.
revision = '89028ebc40d1'
down_revision = '465785295fcb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'title_counts',
        sa.Column('quarter_id', sa.SmallInteger(), nullable=False),
        sa.Column('job_uuid', sa.String(), nullable=False),
        sa.Column('job_title', sa.String(), nullable=True),
        sa.Column('count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['quarter_id'], ['quarters.quarter_id'], ),
        sa.PrimaryKeyConstraint('quarter_id', 'job_uuid')
    )
    op.create_table(
        'geo_title_counts',
        sa.Column('quarter_id', sa.SmallInteger(), nullable=False),
        sa.Column('geography_id', sa.SmallInteger(), nullable=False),
        sa.Column('job_uuid', sa.String(), nullable=False),
        sa.Column('job_title', sa.String(), nullable=True),
        sa.Column('count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['geography_id'], ['geographies.geography_id'], ),
        sa.ForeignKeyConstraint(['quarter_id'], ['quarters.quarter_id'], ),
        sa.PrimaryKeyConstraint('quarter_id', 'geography_id', 'job_uuid')
    )


def downgrade():
    op.drop_table('geo_title_counts')
    op.drop_table('title_counts')
