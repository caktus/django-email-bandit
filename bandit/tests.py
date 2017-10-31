from __future__ import unicode_literals
import six

import asyncore
import platform
import smtpd
import threading
from email import message_from_string
if six.PY3:
    # Python 3
    from email.utils import parseaddr
else:
    # Python 2
    from email.Utils import parseaddr

from django.conf import settings
from django.core.mail import get_connection, EmailMessage
from django.test import TestCase


class FakeSMTPServer(smtpd.SMTPServer, threading.Thread):
    """
    FakeSMTPServer from Django's regressiontests.mail.tests.py

    Asyncore SMTP server wrapped into a thread. Based on DummyFTPServer from:
    http://svn.python.org/view/python/branches/py3k/Lib/test/test_ftplib.py?revision=86061&view=markup
    """

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        if platform.python_version_tuple() >= ("3", "5"):
            kwargs.setdefault('decode_data', True)
        smtpd.SMTPServer.__init__(self, *args, **kwargs)
        self._sink = []
        self.active = False
        self.active_lock = threading.Lock()
        self.sink_lock = threading.Lock()

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        # if not isinstance(data, six.text_type):
        #     data = data.decode('utf-8')
        m = message_from_string(data)
        maddr = parseaddr(m.get('from'))[1]
        if mailfrom != maddr:
            return "553 '%s' != '%s'" % (mailfrom, maddr)
        self.sink_lock.acquire()
        self._sink.append(m)
        self.sink_lock.release()

    def get_sink(self):
        self.sink_lock.acquire()
        try:
            return self._sink[:]
        finally:
            self.sink_lock.release()

    def flush_sink(self):
        self.sink_lock.acquire()
        self._sink[:] = []
        self.sink_lock.release()

    def start(self):
        assert not self.active
        self.__flag = threading.Event()
        threading.Thread.start(self)
        self.__flag.wait()

    def run(self):
        self.active = True
        self.__flag.set()
        while self.active and asyncore.socket_map:
            self.active_lock.acquire()
            asyncore.loop(timeout=0.1, count=1)
            self.active_lock.release()
        asyncore.close_all()

    def stop(self):
        assert self.active
        self.active = False
        self.join()


class BaseBackendTestCase(TestCase):
    """
    Test email interception in the HijackBackend.
    """

    @classmethod
    def setUpClass(cls):
        cls.server = FakeSMTPServer(('127.0.0.1', 0), None)
        settings.EMAIL_HOST = "127.0.0.1"
        settings.EMAIL_PORT = cls.server.socket.getsockname()[1]
        cls._original_admins = settings.ADMINS
        cls._original_bandit = getattr(settings, 'BANDIT_EMAIL', '')
        settings.BANDIT_EMAIL = 'bandit@example.com'
        settings.ADMINS = (('Admin', 'admin@example.com'), )
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        settings.BANDIT_EMAIL = cls._original_bandit
        settings.ADMINS = cls._original_admins

    def setUp(self):
        super(BaseBackendTestCase, self).setUp()
        self.flush_mailbox()

    def tearDown(self):
        self.flush_mailbox()
        super(BaseBackendTestCase, self).tearDown()

    def get_connection(self):
        raise NotImplementedError('Must define in subclass')

    def get_mailbox_content(self):
        return self.server.get_sink()

    def flush_mailbox(self):
        self.server.flush_sink()


class HijackBackendTestCase(BaseBackendTestCase):

    def get_connection(self):
        return get_connection('bandit.backends.smtp.HijackSMTPBackend')

    def test_basic_hijack(self):
        """Emails should be redirected to send to BANDIT_EMAIL."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['bandit@example.com', ])

    def test_send_to_admins(self):
        """Admin emails should not be hijacked."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['admin@example.com', ])

    def test_send_to_mixed(self):
        """Emails with mixed recipients will be hijacked."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com', 'admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['bandit@example.com', ])

    def test_send_multiple(self):
        """Emails with mixed recipients will be hijacked."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com']),
                  EmailMessage('Subject', 'Content', 'from@example.com', ['admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), len(emails))
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['bandit@example.com', ])
        message = messages[1]
        self.assertEqual(message.get_all('to'), ['admin@example.com', ])

    def test_whitelist_domain(self):
        addresses = ['foo@whitelisted.test.com', 'bar@whitelisted.test.com']
        emails = [EmailMessage( 'Subject', 'Content', 'from@example.com', addresses)]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(messages[0].get_all('to'), [', '.join(addresses)])


class LogOnlyBackendTestCase(BaseBackendTestCase):

    def get_connection(self):
        return get_connection('bandit.backends.smtp.LogOnlySMTPBackend')

    def test_basic_hijack(self):
        """Emails should only be logged."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), 0)

    def test_send_to_admins(self):
        """Admin emails should still be sent."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), len(emails))
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['admin@example.com', ])

    def test_send_to_mixed(self):
        """Emails with mixed recipients will only be logged."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com', 'admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), 0)

    def test_send_multiple(self):
        """Only the email to the admin should be sent (the other should be logged)."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com']),
                  EmailMessage('Subject', 'Content', 'from@example.com', ['admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['admin@example.com', ])
