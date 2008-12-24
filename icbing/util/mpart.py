import email
from email.message import Message
from zope.interface import implements
from twisted.mail import imap4

class MPart(object):
    implements(imap4.IMessagePart)
    
    def __init__(self, msg):
        if isinstance(msg, Message):
            self.message = msg
        elif hasattr(msg, 'read'):
            self.message = email.message_from_file(msg)
        else:
            self.message = email.message_from_string(str(msg))
    
    def _get_message(self):
        return self._message
    
    def _set_message(self, msg):
        self._message = msg
        self.length = len(str(msg))
    
    message = property(_get_message, _set_message)
    
    def getHeaders(self, negate, *names):
        raise NotImplementedError
    
    def getBodyFile(self):
        raise NotImplementedError
    
    def getSize(self):
        raise NotImplementedError
    
    def isMultipart(self):
        raise NotImplementedError
    
    def getSubPart(self, part):
        raise NotImplementedError
