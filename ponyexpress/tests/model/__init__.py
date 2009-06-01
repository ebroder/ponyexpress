"""
Tests for the PonyExpress database model
"""

def setup():
    """
    It's pretty hard to do any kind of database testing without having
    a database to test against, so let's make one of those.
    """

    from ponyexpress import model
    import sqlalchemy

    e = sqlalchemy.create_engine('sqlite://')
    model.init_model(e)
    model.Base.metadata.create_all(bind=e)
