"""
ponyexpress utility modules: a class for storing headers
"""

class Headers(object):
    """
    An ordered dictionary look-alike that allows multiple values with
    the same key
    """

    def __init__(self, headers=[]):
        """
        Create a new Headers object.

        headers can be a dict, an email.message.Message instance,
        another Headers instance, or anything that has an .items()
        method. It can also be an iterator over two-tuples
        """
        if hasattr(headers, 'items'):
            self._headers = list(headers.items())
        else:
            self._headers = list(headers)

    def keys(self):
        """
        Return a list of all the header names.
        """
        return list(self.iterkeys())

    def values(self):
        """
        Return a list of all the header values.
        """
        return list(self.itervalues())

    def items(self):
        """
        Return a list of two-tuples of header fields and values.
        """
        return list(self.iteritems())

    def iterkeys(self):
        """
        Return an iterator over all the header names.
        """
        return (k for k, v in self._headers)

    def itervalues(self):
        """
        Return an iterator over all the header values.
        """
        return (v for k, v in self._headers)

    def iteritems(self):
        """
        Return an iterator over all two-tuples of header fields and
        values.
        """
        return ((k, v) for k, v in self._headers)

    def __contains__(self, header):
        """
        Return True if header is in self, else False
        """
        header = header.lower()
        # Use any to avoid iterating over the whole list if it can be
        # helped
        return any((header == k.lower()) for k in self.iterkeys())
    has_key = __contains__

    def ___delitem__(self, item):
        """
        Delete all occurrences of a header, if present.

        Does not raise an exception if the header is missing
        """
        name = name.lower()
        newheaders = []
        for k, v in self._headers:
            if k.lower() != name:
                newheaders.append((k, v))
        self._headers = newheaders

    def __getitem__(self, name):
        """
        Get a header value.

        Raises KeyError if the header is missing.

        If the header name appears multiple times, the first
        occurrence will be returned.
        """
        name = name.lower()
        for k, v in self._headers:
            if k.lower() == name:
                return v
        else:
            raise KeyError, name

    def __setitem__(self, name, val):
        """
        Add a new header with the given value.

        This does not overwrite existing headers with the same name.
        """
        self._headers.append((name, val))

    def __len__(self):
        """
        Return the number of headers in the object.
        """
        return len(self._headers)

    def clear(self):
        """
        Remove all headers.
        """
        self._headers = []

    def get(self, k, x=None):
        """
        Get a header value.

        Like __getitem__(), but returns x if the field is missing
        """
        try:
            return self[k]
        except KeyError:
            return x

    def setdefault(self, k, x=None):
        """
        Get a header value, setting it to x if it doesn't exist
        """
        try:
            return self[k]
        except KeyError:
            self[k] = x
            return x

    def get_all(self, name):
        name = name.lower()
        return [v for k, v in self._headers if k.lower() == name]
