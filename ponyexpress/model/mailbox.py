import sqlalchemy as sa
from sqlalchemy.orm import relation

from ponyexpress.model.base import Base
from ponyexpress.model.tag import Tag
from ponyexpress.model.message import Message
from ponyexpress.model import meta

from zope.interface import implements
from twisted.mail import imap4

class Mailbox(Base):
    __tablename__ = 'mailboxes'
    implements(imap4.IMailbox, imap4.ISearchableMailbox)

    id = sa.Column(sa.types.Integer, primary_key=True)
    path = sa.Column(sa.types.Text, nullable=False)
    set_tag_id = sa.Column(sa.ForeignKey('tags.id'))
    query = sa.Column(sa.types.PickleType, nullable=False)
    """
    The query structure determines which messages are displayed as
    being in this mailbox.

    If query is a string, then it matches all messages tagged with
    that string.

    If it is a number, then it matches all messages tagged with the
    tag whose id is that number.

    If it is a tuple, then the tuple must be of odd length and its
    members must alternate between sub-query specifications and
    operands. Operands are strings and are one of "&" (intersection),
    "|" (union), or "-" (set difference). All operands are processed
    from left to right.

    An example of a query might be::

        ("sipb", "&", "debathena", "-", ("ubuntu", "|", "debian"))
    """

    set_tag = relation(Tag)

    @sa.orm.reconstructor
    def loadContents(self):
        """
        Load the list of Message ids contained in this Mailbox based
        on the query value.
        """
        self.messages = list(self.parseQuery(self.query))
        self.messages.sort()

    @staticmethod
    def parseQuery(query):
        """
        Given a query list or string, return those messages that match
        that query.
        """
        if isinstance(query, basestring):
            return set(meta.Session.query(Message.id).join('tags').\
                           filter_by(name=query))
        elif isinstance(query, int):
            return set(meta.Session.query(Message.id).join('tags').\
                           filter_by(id=query))
        else:
            # I'm going to be manipulating the query list, so I need
            # to duplicate it
            query = list(query)
            # We need somewhere to start from
            messages = self.parseQuery(query.pop(0))
            while query:
                # Evaluate the next query spec
                next = self.parseQuery(query[1])
                # And combine appropriately
                op = query[0]
                if op == '&':
                    messages &= next
                elif op == '|':
                    messages |= next
                elif op == '-':
                    messages -= next

                # Remove the operand and query spec we just processed
                del query[0:2]
            return messages

    # The twisted.mail.imap4.IMailbox interface:

    def getUIDValidity(self):
        # Since the UID is the primary key of the database, that will
        # never change, so the UIDVALIDITY is constant
        return 1

    def getUIDNext(self):
        # It's a bit dumb, but there's no database-independent way to
        # get the next value to be used for a primary key.
        #
        # UIDNEXT isn't guaranteed to be accurate anyway, just
        # guaranteed to change iff new messages get inserted. This
        # method should have that property.
        try:
            return meta.Session.query(sa.func.max(Message.id)).one()[0] + 1
        except TypeError:
            return 1

    def getUID(self, message):
        # self.messages is already a list of UIDs in sequence
        # order. This is easy!
        return self.messages[message]

    def getMessageCount(self):
        # Also easy, since we already have a list of messages in this
        # mailbox
        return len(self.messages)

    def getRecentCount(self):
        # Slightly less easy
        return meta.Session.query(sa.func.count(Message.id)).\
            filter(Message.id.in_(self.messages)).\
            filter(Message.recent==True).one()[0]

    def getUnseenCount(self):
        return meta.Session.query(sa.func.count(Message.id)).\
            filter(Message.id.in_(self.messages)).\
            filter(Message.seen==False).one()[0]

    def isWriteable(self):
        # A mailbox is only writeable if moving a message into it
        # causes that message to be tagged with something
        return self.set_tag is not None

    def destroy(self):
        raise NotImplementedError

    def requestStatus(self, names):
        return imap4.statusRequestHelper(self, names)

    def addListener(self, listener):
        raise NotImplementedError

    def removeListener(self, listener):
        raise NotImplementedError

    def addMessage(self, message, flags={}, date=None):
        raise NotImplementedError

    def expunge(self):
        raise NotImplementedError

    def fetch(self, messages, uid):
        for m in messages:
            if uid:
                yield meta.Session.query(Message).get(m)
            else:
                yield meta.Session.query(Message).get(self.messages[m])

    def store(self, messages, flags, mode, uid):
        raise NotImplementedError

    # The twisted.mail.imap4.ISearchableMailbox interface

    def search(self, query, uid):
        raise NotImplementedError
