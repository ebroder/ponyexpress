import sqlalchemy as sa
from sqlalchemy.orm import relation

from ponyexpress.model.base import Base
from ponyexpress.model.tag import Tag
from ponyexpress.model.message_tag import MessageTag
from ponyexpress.model.message import Message
from ponyexpress.model import meta

from zope.interface import implements
from twisted.mail import imap4

class Mailbox(Base):
    __tablename__ = 'mailboxes'
    implements(imap4.IMailbox, imap4.ISearchableMailbox, imap4.IMessageCopier)

    id = sa.Column(sa.types.Integer, primary_key=True)
    path = sa.Column(sa.types.Text, nullable=False, unique=True)
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

    Whether a folder is writeable is determined by its query string -
    if the string only references a single tag, then moving a message
    into that folder adds that tag. If the query is more complex, then
    the folder is read-only.
    """

    def setTag(self):
        if not isinstance(self.query, (basestring, int)):
            return
        if isinstance(self.query, basestring):
            return meta.Session.query(Tag).filter_by(name=self.query).one()
        else:
            return meta.Session.query(Tag).get(self.query)

    @sa.orm.reconstructor
    def loadContents(self):
        """
        Load the list of Message ids contained in this Mailbox based
        on the query value.
        """
        self.messages = self.parseQuery(self.query).all()
        self.messages.sort()

    @classmethod
    def parseQuery(cls, query):
        """
        Given a query list or string, return those messages that match
        that query.
        """
        if isinstance(query, basestring):
            return meta.Session.query(Message.id).join('tags').\
                filter_by(name=query)
        elif isinstance(query, int):
            return meta.Session.query(Message.id).join('tags').\
                filter_by(id=query)
        else:
            # I'm going to be manipulating the query list, so I need
            # to duplicate it
            query = list(query)
            # We need somewhere to start from
            messages = cls.parseQuery(query.pop(0))
            while query:
                # Evaluate the next query spec
                next = cls.parseQuery(query[1])
                # And combine appropriately
                op = query[0]
                if op == '&':
                    messages = messages.intersect(next)
                elif op == '|':
                    messages = messages.union(next)
                elif op == '-':
                    messages = messages.except_(next)

                # Remove the operand and query spec we just processed
                del query[0:2]
            return messages

    def __terminateSet(self, messages, uid):
        if uid:
            messages.last = self.messages[-1]
        else:
            messages.last = len(self.messages)

    # The twisted.mail.imap4.IMailboxInfo interface (inherited by IMailbox)

    def getFlags(self):
        # Flags required by the IMAP spec
        flags = ['\Answered', '\Flagged', '\Deleted', '\Seen', '\Draft']
        # Keywords already defined as tags
        flags.extend(row[0] for row in meta.Session.query(Tag.name))
        # Indicate that clients can create new keywords
        flags.append('\*')
        return flags

    def getHierarchialDelimiter():
        return '.'

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
        return self.messages[message - 1]

    def getMessageCount(self):
        # Also easy, since we already have a list of messages in this
        # mailbox
        return len(self.messages)

    def getRecentCount(self):
        # Slightly less easy
        return meta.Session.query(Message).\
            filter(Message.id.in_(self.messages)).\
            filter(Message.recent==True).count()

    def getUnseenCount(self):
        return meta.Session.query(Message).\
            filter(Message.id.in_(self.messages)).\
            filter(Message.seen==False).count()

    def isWriteable(self):
        # A mailbox is only writeable if moving a message into it
        # causes that message to be tagged with something
        return isinstance(self.query, (basestring, int))

    def destroy(self):
        try:
            setTag = self.setTag()
            if setTag is not None:
                meta.Session.query(MessageTag).\
                    filter(MessageTag.tag_id==setTag).\
                    delete()
                meta.Session.commit()
        except:
            meta.Session.rollback()
            raise

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
        self.__terminateSet(messages, uid)
        for m in messages:
            if uid:
                # If we're looping over a range of UIDs, we should
                # make sure each UID exists so we don't yield None
                msg = meta.Session.query(Message).get(m)
                if msg is not None:
                    yield msg
            else:
                # The message sequence counter could potentially
                # overflow the number of messages in the mailbox
                try:
                    yield meta.Session.query(Message).get(self.messages[m - 1])
                except KeyError:
                    pass

    def store(self, messages, flags, mode, uid):
        raise NotImplementedError

    # The twisted.mail.imap4.ISearchableMailbox interface

    def search(self, query, uid):
        raise NotImplementedError

    # The twisted.mail.imap4.IMessageCopier interface

    def copy(self, msg):
        # Since msg must have come from IMailbox.fetch, it must be a
        # ponyexpress.model.Message object, so we can just append to
        # its tag list
        try:
            setTag = self.setTag()
            if setTag is None:
                raise imap4.ReadOnlyMailbox
            msg.tags.append(setTag)
            meta.Session.add(msg)
            meta.Session.commit()
            return msg.id
        except:
            meta.Session.rollback()
            raise
