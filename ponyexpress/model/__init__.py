"""The PonyExpress database model"""

from sqlalchemy import orm

from ponyexpress.model.header import Header
from ponyexpress.model.tag import Tag
from ponyexpress.model.message import Message
from ponyexpress.model.mailbox import Mailbox

from ponyexpress.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
