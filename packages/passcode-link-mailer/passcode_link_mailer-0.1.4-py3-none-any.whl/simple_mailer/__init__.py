"""
Simple Passcode Mailer
----------------------

A simple Python library to send email confirmations via Gmail using App Passwords,
featuring a unique passcode and a timed confirmation link.
"""

from .passcode_link_mailer import PasscodeLinkMailer, EmailSendingError, EmailSendingAuthError, EmailSendingConnectionError

__version__ = "0.1.4"
__author__ = "Jonatan Shaya"
__email__ = "Jonatan.shaya99@gmail.com"


__all__ = ['PasscodeLinkMailer', 'EmailSendingError', 'EmailSendingAuthError', 'EmailSendingConnectionError']
