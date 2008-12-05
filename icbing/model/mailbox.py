import sqlalchemy as sa
from sqlalchemy.orm import relation

from icbing.model.base import Base
from icbing.model.tag import Tag

from zope.interface import implements
from twisted.mail import imap4

class Mailbox(Base):
    __tablename__ = 'mailboxes'
    implements(imap4.IMailbox, imap4.ISearchableMailbox)
    
    id = sa.Column(sa.types.Integer, primary_key=True)
    path = sa.Column(sa.types.Text, nullable=False)
    set_tag_id = sa.Column(sa.ForeignKey('tags.id'))
    query = sa.Column(sa.types.PickleType, nullable=False)
    
    set_tag = relation(Tag)
    
    # The twisted.mail.imap4.IMailbox interface:
    
    def getUIDValidity(self):
        raise NotImplementedError
    
    def getUIDNext(self):
        raise NotImplementedError
    
    def getUID(self, message):
        raise NotImplementedError
    
    def getMessageCount(self):
        raise NotImplementedError
    
    def getRecentCount(self):
        raise NotImplementedError
    
    def getUnseenCount(self):
        raise NotImplementedError
    
    def isWriteable(self):
        raise NotImplementedError
    
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
        raise NotImplementedError
    
    def store(self, messages, flags, mode, uid):
        raise NotImplementedError
    
    # The twisted.mail.imap4.ISearchableMailbox interface
    
    def search(self, query, uid):
        raise NotImplementedError
