import sqlalchemy as sa

from ponyexpress.model.base import Base

class MessageTag(Base):
    __tablename__ = 'messages_tags'

    id = sa.Column(sa.types.Integer, primary_key=True)
    message_id = sa.Column(sa.ForeignKey('messages.id', ondelete='CASCADE', onupdate='CASCADE'))
    tag_id = sa.Column(sa.ForeignKey('tags.id', ondelete='CASCADE', onupdate='CASCADE'))
    deleted = sa.Column(sa.types.Boolean, nullable=False, default=False)
