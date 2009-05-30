import sqlalchemy as sa
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

from ponyexpress.model.base import Base
from ponyexpress.model.message_tag import MessageTag

class Tag(Base):
    __tablename__ = 'tags'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Unicode(255), nullable=False, index=True,
                     unique=True)
    tag_messages = relation(MessageTag, backref='tag')
    messages = association_proxy('tag_messages', 'message',
                                 creator=(lambda x: MessageTag(message=x)))
