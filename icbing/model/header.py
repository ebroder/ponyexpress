import sqlalchemy as sa
from sqlalchemy.orm import relation
from icbing.model.base import Base

class Header(Base):
    __tablename__ = 'headers'
    
    id = sa.Column(sa.types.Integer, primary_key=True)
    position = sa.Column(sa.types.Integer)
    message_id = sa.Column(sa.ForeignKey('messages.id'))
    field = sa.Column(sa.types.Unicode(255))
    value = sa.Column(sa.types.UnicodeText)
