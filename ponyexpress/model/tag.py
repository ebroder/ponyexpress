import sqlalchemy as sa
from sqlalchemy.orm import relation
from ponyexpress.model.base import Base

class Tag(Base):
    __tablename__ = 'tags'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Unicode(255), nullable=False, index=True,
                     unique=True)
