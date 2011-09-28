import asyncore
import email
import smtpd
import threading

from django.conf import settings
from django.core.mail import get_connection, EmailMessage
from django.template.loader import render_to_string
from django.test import TestCase


class FakeSMTPServer(smtpd.SMTPServer, threading.Thread):
    """
    FakeSMTPServer from Django's regressiontests.mail.tests.py

    Asyncore SMTP server wrapped into a thread. Based on DummyFTPServer from:
    http://svn.python.org/view/python/branches/py3k/Lib/test/test_ftplib.py?revision=86061&view=markup
    """

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        smtpd.SMTPServer.__init__(self, *args, **kwargs)
        self._sink = []
        self.active = False
        self.active_lock = threading.Lock()
        self.sink_lock = threading.Lock()

    def process_message(self, peer, mailfrom, rcpttos, data):
        m = email.message_from_string(data)
        maddr = email.Utils.parseaddr(m.get('from'))[1]
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


class HijackBackendTestCase(TestCase):
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
        super(HijackBackendTestCase, self).setUp()
        self.flush_mailbox()

    def tearDown(self):
        self.flush_mailbox()
        super(HijackBackendTestCase, self).tearDown()

    def get_connection(self):
        return get_connection('bandit.backends.HijackBackend')

    def get_mailbox_content(self):
        return self.server.get_sink()

    def flush_mailbox(self):
        self.server.flush_sink()

    def test_basic_hijack(self):
        """Emails should be redirected to send to BANDIT_EMAIL."""
        email = EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])
        num_sent = self.get_connection().send_messages([email, ])
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['bandit@example.com', ])

    def test_send_to_admins(self):
        """Admin emails should not be hijacked."""
        email = EmailMessage('Subject', 'Content', 'from@example.com', ['admin@example.com'])
        num_sent = self.get_connection().send_messages([email, ])
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['admin@example.com', ])

    def test_send_to_mixed(self):
        """Emails with mixed recipients will be hijacked."""
        email = EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com', 'admin@example.com'])
        num_sent = self.get_connection().send_messages([email, ])
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['bandit@example.com', ])
