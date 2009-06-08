import sqlalchemy as sa
from sqlalchemy.orm import relation, deferred
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from ponyexpress.model.base import Base
from ponyexpress.model.header import Header
from ponyexpress.model.message_tag import MessageTag

from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'sqlite_autoincrement': True}

    # Used as the UID of the message
    id = sa.Column(sa.types.Integer, primary_key=True)
    # Just the message body; does not include headers
    body = deferred(sa.Column(sa.types.Text, index=True))
    # This is the total size of the message, including headers, in
    # bytes when rendered in RFC 2822 form
    length = sa.Column(sa.types.Integer, nullable=False)
    deleted = sa.Column(sa.types.Boolean, nullable=False, default=False)

    # Used for the internal date field
    created_at = sa.Column(sa.types.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.types.DateTime, onupdate=datetime.utcnow)

    headers = relation(Header,
                       backref='message',
                       collection_class=ordering_list('position'),
                       cascade='all, delete-orphan',
                       order_by=[Header.position])
    message_tags = relation(MessageTag,
                            backref='message',
                            collection_class=set,
                            cascade='all, delete-orphan')
    tags = association_proxy('message_tags', 'tag',
                             creator=(lambda x: MessageTag(tag=x)))
