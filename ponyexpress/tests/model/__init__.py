"""
Tests for the PonyExpress database model
"""

from ponyexpress import model
import sqlalchemy

def setup():
    """
    It's pretty hard to do any kind of database testing without having
    a database to test against, so let's make one of those.
    """

    e = sqlalchemy.create_engine('sqlite://')
    model.init_model(e)
    model.Base.metadata.create_all(bind=e)

def clearTables():
    for t in dir(model):
        try:
            if t != 'Base' and issubclass(getattr(model, t), model.Base):
                for x in model.meta.Session.query(getattr(model, t)):
                    model.meta.Session.delete(x)
        except TypeError:
            pass
    model.meta.Session.commit()
