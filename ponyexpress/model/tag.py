import sqlalchemy as sa
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

from ponyexpress.model.base import Base
from ponyexpress.model.message_tag import MessageTag
from ponyexpress.model import meta

from zope.interface import implements
from twisted.mail import imap4

class Tag(Base):
    __tablename__ = 'tags'
    # For each tag, there is an associated mailbox - this class
    # implements that interface
    implements(imap4.IMailbox)

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Unicode(255), nullable=False, index=True,
                     unique=True)
    tag_messages = relation(MessageTag, backref='tag')
    messages = association_proxy('tag_messages', 'message',
                                 creator=(lambda x: MessageTag(message=x)))
