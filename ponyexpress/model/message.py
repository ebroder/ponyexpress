import sqlalchemy as sa
from sqlalchemy.orm import relation
from sqlalchemy.ext.orderinglist import ordering_list

from ponyexpress.model.base import Base
from ponyexpress.model.header import Header
from ponyexpress.model.tag import Tag
from ponyexpress.model.message_tag import messages_tags

from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'

    # Used as the UID of the message
    id = sa.Column(sa.types.Integer, primary_key=True)
    # Just the message body; does not include headers
    body = sa.Column(sa.types.Text, index=True)
    # This is the total size of the message, including headers, in
    # bytes when rendered in RFC 2822 form
    length = sa.Column(sa.types.Integer, nullable=False)

    seen = sa.Column(sa.types.Boolean, nullable=False, default=False)
    answered = sa.Column(sa.types.Boolean, nullable=False, default=False)
    flagged = sa.Column(sa.types.Boolean, nullable=False, default=False)
    deleted = sa.Column(sa.types.Boolean, nullable=False, default=False)
    draft = sa.Column(sa.types.Boolean, nullable=False, default=False)
    recent = sa.Column(sa.types.Boolean, nullable=False, default=True)

    # Used for the internal date field
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
