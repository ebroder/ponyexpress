import sqlalchemy as sa
from sqlalchemy.orm import relation
from sqlalchemy.ext.orderinglist import ordering_list

from icbing.model.base import Base
from icbing.model.header import Header
from icbing.model.tag import Tag
from icbing.model.message_tag import messages_tags

from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'
    
    id = sa.Column(sa.types.Integer, primary_key=True)
    orig_body = sa.Column(sa.types.Binary)
    length = sa.Column(sa.types.Integer, nullable=False)
    search_body = sa.Column(sa.types.Text, index=True)
    
    seen = sa.Column(sa.types.Boolean, nullable=False, default=False)
    answered = sa.Column(sa.types.Boolean, nullable=False, default=False)
    flagged = sa.Column(sa.types.Boolean, nullable=False, default=False)
    deleted = sa.Column(sa.types.Boolean, nullable=False, default=False)
    draft = sa.Column(sa.types.Boolean, nullable=False, default=False)
    recent = sa.Column(sa.types.Boolean, nullable=False, default=True)
    
    created_at = sa.Column(sa.types.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.types.DateTime, onupdate=datetime.utcnow)
    
    headers = relation(Header,
                       backref='message',
                       collection_class=ordering_list('position'),
                       cascade='all, delete-orphan',
                       order_by=[Header.position])
    tags = relation(Tag,
                    backref='messages',
                    secondary=messages_tags)
