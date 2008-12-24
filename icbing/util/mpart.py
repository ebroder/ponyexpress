import email
from email.message import Message
from zope.interface import implements
from twisted.mail import imap4

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from icbing.util.headers import Headers

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
        if len(names) == 0:
            # No names specified and negate is True means return
            # nothing
            if negate: return {}
            # No names specified and negate is False means return
            # everything, or exclude nothing. The logic behind an
            # empty names list makes sense if we just switch the
            # negate flag
            else: negate = True
        
        headers = Headers()
        for k, v in self.message.items():
            # Use an exclusive or to simplify the logic
            if k in names is not negate:
                headers[k] = v
        
        return headers
    
    def getBodyFile(self):
        return StringIO(str(self.message.get_payload()))
    
    def getSize(self):
        return self.length
    
    def isMultipart(self):
        return self.message.is_multipart()
    
    def getSubPart(self, part):
        return MPart(self.message.get_payload(part))
