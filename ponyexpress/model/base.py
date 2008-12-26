"""The base for declarative-style models"""

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

Base = declarative_base()

__all__ = ['Base']
