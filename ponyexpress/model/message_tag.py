import sqlalchemy as sa

from ponyexpress.model.base import Base

messages_tags = sa.Table('messages_tags', Base.metadata,
                         sa.Column('message_id', sa.ForeignKey('messages.id'), primary_key=True),
                         sa.Column('tag_id', sa.ForeignKey('tags.id'), primary_key=True))
