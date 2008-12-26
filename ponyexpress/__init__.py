"""
The PonyExpress

An IMAP server with ponies.

PonyExpress provides the tagging/labelling features similar to the
Gmail IMAP server. All folders are virtual folders. Moving messages
into that folder adds some tag to the message; deleting a message in a
folder removes that tag. The contents of a folder are dynamically
generated based on a query associated with the folder.

By default, a folder corresponds to a tag of the same name, and shows
all messages with that tag.

For fast access and easy tag management, all e-mail is stored in a
database.

PonyExpress also provides a series of scripts for managing messages
from the command line or procmail.
"""
