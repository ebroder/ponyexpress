import sqlalchemy as sa
from sqlalchemy.orm import relation

from ponyexpress.model.base import Base
from ponyexpress.model.tag import Tag

class MessageTag(Base):
    __tablename__ = 'messages_tags'

    message_id = sa.Column(sa.ForeignKey('messages.id'), primary_key=True)
    tag_id = sa.Column(sa.ForeignKey('tags.id'), primary_key=True)
    deleted = sa.Column(sa.types.Boolean, nullable=False, default=False)
    tag = relation(Tag)
