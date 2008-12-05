import sqlalchemy as sa
from sqlalchemy.orm import relation

from icbing.model.base import Base
from icbing.model.tag import Tag

class Folder(Base):
    __tablename__ = 'folders'
    
    id = sa.Column(sa.types.Integer, primary_key=True)
    path = sa.Column(sa.types.Text, nullable=False)
    set_tag_id = sa.Column(sa.ForeignKey('tags.id'))
    query = sa.Column(sa.types.PickleType, nullable=False)
    
    set_tag = relation(Tag)
