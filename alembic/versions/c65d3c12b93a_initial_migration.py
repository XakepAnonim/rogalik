"""Initial migration

Revision ID: c65d3c12b93a
Revises: 
Create Date: 2024-12-01 17:38:11.744315

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c65d3c12b93a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buff',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('debuff',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player',
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_email'), 'player', ['email'], unique=True)
    op.create_index(op.f('ix_player_username'), 'player', ['username'], unique=True)
    op.create_table('race',
    sa.Column('type', sa.String(length=6), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skill',
    sa.Column('type', sa.String(length=8), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('required_level', sa.Integer(), nullable=False),
    sa.Column('cooldown', sa.Integer(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('character',
    sa.Column('game_name', sa.String(length=32), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('health', sa.Integer(), nullable=False),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.Column('stamina', sa.Integer(), nullable=False),
    sa.Column('damage', sa.Integer(), nullable=False),
    sa.Column('armor', sa.Integer(), nullable=False),
    sa.Column('skill_points', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.UUID(), nullable=True),
    sa.Column('class_id', sa.UUID(), nullable=True),
    sa.Column('race_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class_buff',
    sa.Column('class_id', sa.UUID(), nullable=True),
    sa.Column('buff_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['buff_id'], ['buff.id'], ),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], )
    )
    op.create_table('class_debuff',
    sa.Column('class_id', sa.UUID(), nullable=True),
    sa.Column('debuff_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['debuff_id'], ['debuff.id'], )
    )
    op.create_table('effect',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('skill_id', sa.UUID(), nullable=True),
    sa.Column('character_class_id', sa.UUID(), nullable=True),
    sa.Column('race_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['character_class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('race_buff',
    sa.Column('race_id', sa.UUID(), nullable=True),
    sa.Column('buff_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['buff_id'], ['buff.id'], ),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], )
    )
    op.create_table('race_debuff',
    sa.Column('race_id', sa.UUID(), nullable=True),
    sa.Column('debuff_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['debuff_id'], ['debuff.id'], ),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], )
    )
    op.create_table('character_skill',
    sa.Column('character_id', sa.UUID(), nullable=True),
    sa.Column('skill_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('character_skill')
    op.drop_table('race_debuff')
    op.drop_table('race_buff')
    op.drop_table('effect')
    op.drop_table('class_debuff')
    op.drop_table('class_buff')
    op.drop_table('character')
    op.drop_table('skill')
    op.drop_table('race')
    op.drop_index(op.f('ix_player_username'), table_name='player')
    op.drop_index(op.f('ix_player_email'), table_name='player')
    op.drop_table('player')
    op.drop_table('debuff')
    op.drop_table('class')
    op.drop_table('buff')
    # ### end Alembic commands ###