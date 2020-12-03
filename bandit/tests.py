from __future__ import unicode_literals

import asyncore
import platform
import smtpd
import threading

from email import message_from_string
from email.utils import parseaddr

from django.conf import settings
from django.core.mail import get_connection, EmailMessage
from django.test import TestCase, override_settings


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


@override_settings(BANDIT_EMAIL='bandit@example.com')
@override_settings(ADMINS=(('Admin', 'admin@example.com'),))
class BaseBackendTestCase(TestCase):
    """
    Test email interception in the HijackBackend.
    """

    @classmethod
    def setUpClass(cls):
        cls.server = FakeSMTPServer(('127.0.0.1', 0), None)
        settings.EMAIL_HOST = "127.0.0.1"
        settings.EMAIL_PORT = cls.server.socket.getsockname()[1]
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

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

    def assert_emails_are_hijacked(self, emails):
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        if isinstance(settings.BANDIT_EMAIL, list):
            self.assertEqual(messages[0].get_all('to')[0].replace('\n', ''), ', '.join(settings.BANDIT_EMAIL))
        else:
            self.assertEqual(messages[0].get_all('to'), ['bandit@example.com', ])

    def test_basic_hijack(self):
        """Emails should be redirected to send to BANDIT_EMAIL."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])]
        self.assert_emails_are_hijacked(emails)

    @override_settings(BANDIT_EMAIL=['bandit@example.com', 'accomplice@example.com', 'Hijacker <hijacker@example.com>'])
    def test_send_to_multiple_bandits(self):
        """Emails should be redirected to all bandit emails."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])]
        self.assert_emails_are_hijacked(emails)

    def test_hijack_cc(self):
        """Emails with unapproved recipient in CC should be redirected to send to BANDIT_EMAIL."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', to=['admin@example.com'], cc=['to@example.com'])]
        self.assert_emails_are_hijacked(emails)

    def test_hijack_bcc(self):
        """Emails with unapproved recipient in BCC should be redirected to send to BANDIT_EMAIL."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', to=['admin@example.com'], bcc=['to@example.com'])]
        self.assert_emails_are_hijacked(emails)

    def test_send_to_mixed(self):
        """Emails with mixed recipients will be hijacked."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com', 'admin@example.com'])]
        self.assert_emails_are_hijacked(emails)

    def test_send_to_admins(self):
        """Admin emails should not be hijacked."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['admin@example.com', ])

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
        """Emails send to whitelisted domains should not be hijacked"""
        addresses = ['foo@whitelisted.test.com',
                     '<bar@whitelisted.test.com>',
                     'Foo Bar <baz@whitelisted.test.com>']
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', addresses)]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(messages[0].get_all('to')[0].replace('\n', ''), ', '.join(addresses))

    @override_settings(
        BANDIT_REGEX_WHITELIST=["ba.*it@bandit\\.com", "joe@.*\\.org"]
    )
    def test_whitelist_email_regex(self):
        """Emails send to whitelisted by regex should not be hijacked"""
        addresses = ['bandit@bandit.com',
                     '<joe@bandit.org>',
                     'Foo Bar <joe@joe.org>']
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', addresses)]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(messages[0].get_all('to')[0].replace('\n', ''), ', '.join(addresses))

    @override_settings(
        BANDIT_REGEX_WHITELIST=["ba.*it@bandit\\.com", "joe@.*\\.org"]
    )
    def test_whitelist_email_regex_not_passing(self):
        """Emails that don't match whitelist regex should be hijacked"""
        addresses = ['joe@bandit.com',
                     '<joe@bandit.com>',
                     'Foo Bar <joe@bandit.com>']
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', addresses)]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(messages[0].get_all('to')[0].replace('\n', ''), 'bandit@example.com')


class LogOnlyBackendTestCase(BaseBackendTestCase):

    def get_connection(self):
        return get_connection('bandit.backends.smtp.LogOnlySMTPBackend')

    def assert_emails_are_only_logged(self, emails):
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), 0)

    def test_basic_hijack(self):
        """Emails should only be logged."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])]
        self.assert_emails_are_only_logged(emails)

    @override_settings(BANDIT_EMAIL=['bandit@example.com', 'accomplice@example.com', 'Hijacker <hijacker@example.com>'])
    def test_send_to_multiple_bandits(self):
        """Even with multiple bandit emails the email are only logged."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])]
        self.assert_emails_are_only_logged(emails)

    def test_hijack_cc(self):
        """Emails with unapproved recipient in CC should only be logged."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', to=['admin@example.com'], cc=['to@example.com'])]
        self.assert_emails_are_only_logged(emails)

    def test_hijack_bcc(self):
        """Emails with unapproved recipient in BCC should only be logged."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', to=['admin@example.com'], bcc=['to@example.com'])]
        self.assert_emails_are_only_logged(emails)

    def test_send_to_mixed(self):
        """Emails with mixed recipients will only be logged."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com', 'admin@example.com'])]
        self.assert_emails_are_only_logged(emails)

    def test_send_to_admins(self):
        """Admin emails should still be sent."""
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', ['admin@example.com'])]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), len(emails))
        message = messages[0]
        self.assertEqual(message.get_all('to'), ['admin@example.com', ])

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

    def test_whitelist_domain(self):
        """Emails send to whitelisted domains are still sent"""
        addresses = ['foo@whitelisted.test.com',
                     '<bar@whitelisted.test.com>',
                     'Foo Bar <baz@whitelisted.test.com>']
        emails = [EmailMessage('Subject', 'Content', 'from@example.com', addresses)]
        num_sent = self.get_connection().send_messages(emails)
        self.assertEqual(len(emails), num_sent)
        messages = self.get_mailbox_content()
        self.assertEqual(len(messages), num_sent)
        self.assertEqual(messages[0].get_all('to')[0].replace('\n', ''), ', '.join(addresses))
