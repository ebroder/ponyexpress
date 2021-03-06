"""
Tests for the PonyExpress Tag model
"""

from ponyexpress.model import *
from ponyexpress.tests.model import ModelTest
from twisted.mail.imap4 import MessageSet
from nose import tools as n

class TestTag(ModelTest):
    def test_getFlags(self):
        t1 = Tag(name=u'foo')
        t2 = Tag(name=u'bar')

        meta.Session.add_all([t1, t2])
        meta.Session.commit()

        n.eq_(len(t1.getFlags()), 4)
        n.eq_(len(t2.getFlags()), 4)

    def test_getUIDValidity(self):
        # Test that the UIDVALIDITY changes when a folder is deleted
        t1 = Tag(name=u'foo')
        meta.Session.add(t1)
        meta.Session.commit()

        oldUIDValidity = t1.getUIDValidity()

        meta.Session.delete(t1)
        meta.Session.commit()

        t2 = Tag(name=u'foo')
        meta.Session.add(t2)
        meta.Session.commit()

        n.ok_(oldUIDValidity < t2.getUIDValidity())

    def test_getUIDNext(self):
        t1 = Tag(name=u'foo')
        t2 = Tag(name=u'bar')

        meta.Session.add_all([t1, t2])
        meta.Session.commit()

        n.eq_(t1.getUIDNext(), 1)

        m1 = Message(body=u'm1', length=0, tags=[t1, t2])
        m2 = Message(body=u'm2', length=0, tags=[t2])

        meta.Session.add_all([m1, m2])
        meta.Session.commit()

        oldUIDNext = t1.getUIDNext()

        m2.tags.add(t1)
        meta.Session.commit()

        n.ok_(oldUIDNext < t1.getUIDNext())
        oldUIDNext = t1.getUIDNext()

        # UIDNEXT shouldn't increase when a message is added to a
        # different folder
        m3 = Message(body=u'm3', length=0, tags=[t2])
        meta.Session.add(m3)
        meta.Session.commit()

        n.eq_(oldUIDNext, t1.getUIDNext())

        m4 = Message(body=u'm4', length=0, tags=[t1])
        meta.Session.add(m4)
        meta.Session.commit()

        n.ok_(oldUIDNext < t1.getUIDNext())

    def test_getMessageCount(self):
        t1 = Tag(name=u'foo')
        t2 = Tag(name=u'bar')

        m1 = Message(body=u"", length=0, tags=[t1])
        m2 = Message(body=u"", length=0, tags=[t1, t2])

        meta.Session.add_all([t1, t2, m1, m2])
        meta.Session.commit()

        n.eq_(t1.getMessageCount(), 2)
        n.eq_(t2.getMessageCount(), 1)
        meta.Session.expunge_all()
        # Make sure that getMessageCount works if the object isn't in the
        # cache
        n.eq_(meta.Session.query(Tag).filter_by(name=u'foo').one().\
                  getMessageCount(), 2)

    def test_getUnseenCount(self):
        seen = Tag(name=ur'\Seen')
        t1 = Tag(name=u'foo')
        t2 = Tag(name=u'bar')

        m1 = Message(body=u"m1", length=0, tags=[seen, t1])
        m2 = Message(body=u"m2", length=0, tags=[t2])
        m3 = Message(body=u"m3", length=0, tags=[t1, t2])

        meta.Session.add_all([seen, t1, t2, m1, m2, m3])
        meta.Session.commit()

        n.eq_(t1.getUnseenCount(), 1)
        n.eq_(t2.getUnseenCount(), 2)

    def test_fetch(self):
        t1 = Tag(name=u'foo')

        m1 = Message(body=u'm1', length=0, tags=[t1])
        m2 = Message(body=u'm2', length=0, tags=[t1])

        meta.Session.add_all([t1, m1, m2])
        meta.Session.commit()

        m = MessageSet(1, 2)
        n.eq_(list(t1.fetch(m, False)), [m1, m2])

        m = MessageSet()
        m.add(t1.getUID(1))
        m.add(t1.getUID(2))
        n.eq_(list(t1.fetch(m, True)), [m1, m2])

    def test_copy(self):
        t1 = Tag(name=u'foo')
        t2 = Tag(name=u'bar')

        m1 = Message(body=u"m1", length=0, tags=[t1])

        meta.Session.add_all([t1, t2, m1])
        meta.Session.commit()

        t2.copy(m1)

        n.ok_(t1 in m1.tags)
        n.ok_(t2 in m1.tags)

    # Tests that I feel idiotic for writing, but will do so anyway so
    # I can boast about coverage

    def test_getHierarchialDelimiter(self):
        t1 = Tag(name=u'foo')
        meta.Session.add(t1)
        meta.Session.commit()

        n.eq_(t1.getHierarchialDelimiter(), '.')

    def test_getRecentCount(self):
        t1 = Tag(name=u'foo')
        meta.Session.add(t1)
        meta.Session.commit()

        n.eq_(t1.getRecentCount(), 0)

    def test_isWriteable(self):
        t1 = Tag(name=u'foo')
        meta.Session.add(t1)
        meta.Session.commit()

        n.eq_(t1.isWriteable(), True)

    def test_destroy(self):
        # There's not actually anything at all to test here, except
        # that the function runs
        t1 = Tag(name=u'foo')
        meta.Session.add(t1)
        meta.Session.commit()

        t1.destroy()
