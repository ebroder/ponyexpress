import sqlalchemy as sa
from sqlalchemy.orm import relation
from icbing.model.base import Base

class Tag(Base):
    __tablename__ = 'tags'
    
    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Unicode(255))

class MessageTag(Base):
    __tablename__ = 'messages_tags'
    
    message_id = sa.Column(sa.ForeignKey('messages.id'), primary_key=True)
    tag_id = sa.Column(sa.ForeignKey('tags.id'), primary_key=True)
