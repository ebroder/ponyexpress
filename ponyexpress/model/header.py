import sqlalchemy as sa
from sqlalchemy.orm import relation
from ponyexpress.model.base import Base

class Header(Base):
    __tablename__ = 'headers'
    __table_args__ = {'sqlite_autoincrement': True}

    id = sa.Column(sa.types.Integer, primary_key=True)
    position = sa.Column(sa.types.Integer)
    message_id = sa.Column(sa.ForeignKey('messages.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    field = sa.Column(sa.types.Unicode(255), nullable=False)
    value = sa.Column(sa.types.UnicodeText, nullable=False)
