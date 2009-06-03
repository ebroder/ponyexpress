"""
Tests for the PonyExpress Tag model
"""

from ponyexpress.model import *
from ponyexpress.tests.model import clearTables

def test_getFlags():
    t1 = Tag(name=u'foo')
    t2 = Tag(name=u'bar')

    meta.Session.add_all([t1, t2])
    meta.Session.commit()

    assert len(t1.getFlags()) == \
        len(t2.getFlags()) == \
        4

    clearTables()

def test_getUIDValidity():
    # Test that the UIDVALIDITY changes when a folder is deleted
    t1 = Tag(name=u'foo')
    meta.Session.add(t1)
    meta.Session.commit()

    oldUIDValidity = t1.getUIDValidity()

    meta.Session.delete(t1)
    meta.Session.commit()

    t2 = Tag(name=u'foo')
    meta.Session.add(t2)

    assert oldUIDValidity != t2.getUIDValidity()

    clearTables()

def test_getMessageCount():
    t1 = Tag(name=u'foo')
    t2 = Tag(name=u'bar')

    m1 = Message(body=u"", length=0, tags=[t1])
    m2 = Message(body=u"", length=0, tags=[t1, t2])

    meta.Session.add_all([t1, t2, m1, m2])
    meta.Session.commit()

    assert t1.getMessageCount() == 2
    assert t2.getMessageCount() == 1
    meta.Session.expunge_all()
    # Make sure that getMessageCount works if the object isn't in the
    # cache
    assert meta.Session.query(Tag).filter_by(name=u'foo').one().getMessageCount() == 2

    clearTables()

def test_getUnseenCount():
    seen = Tag(name=ur'\Seen')
    t1 = Tag(name=u'foo')
    t2 = Tag(name=u'bar')

    m1 = Message(body=u"m1", length=0, tags=[seen, t1])
    m2 = Message(body=u"m2", length=0, tags=[t2])
    m3 = Message(body=u"m3", length=0, tags=[t1, t2])

    meta.Session.add_all([seen, t1, t2, m1, m2, m3])
    meta.Session.commit()

    assert t1.getUnseenCount() == 1
    assert t2.getUnseenCount() == 2

    clearTables()

def test_copy():
    t1 = Tag(name=u'foo')
    t2 = Tag(name=u'bar')

    m1 = Message(body=u"m1", length=0, tags=[t1])

    meta.Session.add_all([t1, t2, m1])
    meta.Session.commit()

    t2.copy(m1)

    assert t1 in m1.tags
    assert t2 in m1.tags

    clearTables()
