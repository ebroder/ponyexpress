import sqlalchemy as sa
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

from ponyexpress.model.base import Base
from ponyexpress.model.message_tag import MessageTag
from ponyexpress.model import meta

from zope.interface import implements
from twisted.mail import imap4

class Tag(Base):
    __tablename__ = 'tags'
    # For each tag, there is an associated mailbox - this class
    # implements that interface
    implements(imap4.IMailbox)

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Unicode(255), nullable=False, index=True,
                     unique=True)
    tag_messages = relation(MessageTag, backref='tag', collection_class=set)
    messages = association_proxy('tag_messages', 'message',
                                 creator=(lambda x: MessageTag(message=x)))

    def __parseSet(self, messages, uid):
        """
        Convert any MessageSet to something more generally usable

        @type C{twisted.mail.imap4.MessageSet}
        @param messages: An object representifying the identifiers to
        iterate over, such as the one passed to
        C{twisted.mail.imap4.fetch}

        @type C{bool}
        @param uid: Whether the IDs in messages are UIDs or message
        sequence IDs.

        @rtype: An iterable of UIDs
        """
        if uid:
            last = meta.Session.query(sa.func.max(MessageTag.id)).\
                filter(MessageTag.tag_id==self.id).scalar()
            if last is None:
                return
            else:
                messages.last = last
                for m in messages:
                    yield m
        else:
            last = meta.Session.query(MessageTag).\
                filter(MessageTag.tag_id==self.id).\
                count()
            if last is 0:
                return
            else:
                messages.last = last
                # TODO: Make this not as retardedly inefficient
                #
                # It'll currently generate one query per message
                # sequence number.
                for m in messages:
                    yield self.getUID(m)

    # The twisted.mail.imap4.IMailboxInfo interface (inherited by IMailbox)

    def getFlags(self):
        # Flags required by the IMAP spec, but not tracked as tags
        flags = ['\Deleted']
        # Keywords already defined as tags
        flags.extend(row[0] for row in meta.Session.query(Tag.name))
        # And indicate that clients can create new keywords
        flags.append('\*')
        return flags

    def getHierarchialDelimiter(self):
        return '.'

    # The twisted.mail.imap4.IMailboxInfo interface (inherited by IMailbox)

    def getUIDValidity(self):
        # We do have to be concerned with a tag being deleted and then
        # recreated, but the UIDVALIDITY value can be constant for a
        # given instance of a folder's lifetime.
        #
        # Hey - that sounds like the Tag primary key!
        return self.id

    def getUIDNext(self):
        # It's kind of dumb, but there's no database-independent way
        # to get the next value that's going to be used for a primary
        # key.
        #
        # UIDNEXT isn't guaranteed to be accurate, just guaranteed to
        # change iff new messages get inserted. This method should
        # have that property.
        #
        # For normal folders, we use the MessageTag.id field as the
        # UID
        try:
            # If there are no messages in this folder, this query will
            # return None, which will throw a TypeError when I try to
            # increment it
            return meta.Session.query(sa.func.max(MessageTag.id)).\
                filter(MessageTag.tag==self).\
                scalar() + 1
        except TypeError:
            return 1

    def getUID(self, message):
        return meta.Session.query(MessageTag.id).\
            filter(MessageTag.tag_id==self.id).\
            offset(message - 1).\
            scalar()

    def getMessageCount(self):
        return len(self.messages)

    def getRecentCount(self):
        # For the time being, PonyExpress never sets the \Recent flag
        # on messages. Since clients are obligated to function without
        # it ever being set, this seems more or less reasonable.
        #
        # Imagine that there was a client that always saw the newest
        # message faster than you did
        return 0

    def getUnseenCount(self):
        return meta.Session.query(Message).\
            filter(Message.id.in_(self.messages)).\
            filter(~Message.message_tags.any(MessageTag.tag.has(name='\\Seen'))).\
            count()
