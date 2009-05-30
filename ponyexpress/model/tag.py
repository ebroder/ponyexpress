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
    tag_messages = relation(MessageTag, backref='tag')
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
                    yield meta.Session.query(MessageTag.id).\
                        filter(MessageTag.tag_id==self.id).\
                        offset(m - 1).\
                        scalar()

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
