import sqlalchemy as sa
from sqlalchemy.orm import relation
from sqlalchemy.ext.orderinglist import ordering_list

from icbing.model.base import Base
from icbing.model.header import Header
from icbing.model.tag import Tag

from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'
    
    id = sa.Column(sa.types.Integer, primary_key=True)
    orig_body = sa.Column(sa.types.Binary)
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
                       order_by=[Header.position])
    tags = relation(Tag,
                    backref='tags',
                    secondary='MessageTag')

# This class has to be defined after both Message and Tag are defined
# - sa.orm.relation() is clever enough to take strings for classes
# that aren't defined, but sa.ForeignKey expects the foreign key's
# table object to already be defined in the mapper
class MessageTag(Base):
    __tablename__ = 'messages_tags'
    
    message_id = sa.Column(sa.ForeignKey('messages.id'), primary_key=True)
    tag_id = sa.Column(sa.ForeignKey('tags.id'), primary_key=True)
