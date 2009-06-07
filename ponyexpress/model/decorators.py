"""
Utility decorators for functions and methods that interact with the
PonyExpress models
"""

from ponyexpress.model import meta
from decorator import decorator

@decorator
def in_transaction(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
        meta.Session.commit()
    except:
        meta.Session.rollback()
        raise
