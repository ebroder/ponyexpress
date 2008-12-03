import sqlalchemy as sa
from sqlalchemy.orm import relation
from sqlalchemy.ext.orderinglist import ordering_list

from icbing.model.base import Base
from icbing.model.header import Header
from icbing.model.tag import Tag

import datetime

class Message(Base):
    __tablename__ = 'messages'
    
    id = sa.Column(sa.types.Integer, primary_key=True)
    orig_body = sa.Column(sa.types.Binary)
    search_body = sa.Column(sa.types.Text, index=True)
    
    seen = sa.Column(sa.types.Boolean, default=False)
    answered = sa.Column(sa.types.Boolean, default=False)
    flagged = sa.Column(sa.types.Boolean, default=False)
    deleted = sa.Column(sa.types.Boolean, default=False)
    draft = sa.Column(sa.types.Boolean, default=False)
    recent = sa.Column(sa.types.Boolean, default=True)
    
    created_at = sa.Column(sa.types.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.types.DateTime, onupdate=datetime.utcnow)
    
    headers = relation(Header,
                       backref='message',
                       collection_class=ordering_list('position'),
                       order_by=[Header.position],
                       ondelete='all, delete-orphan')
    tags = relation(Tag,
                    backref='tags',
                    secondary='MessageTag')

class MessageTag(Base):
    __tablename__ = 'messages_tags'
    
    message_id = sa.Column(sa.ForeignKey('messages.id'), primary_key=True)
    tag_id = sa.Column(sa.ForeignKey('tags.id'), primary_key=True)
