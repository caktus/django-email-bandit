from __future__ import unicode_literals

from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

from bandit.backends.base import HijackBackendMixin, LogOnlyBackendMixin


class HijackSMTPBackend(HijackBackendMixin, SMTPBackend):
    """
    This backend intercepts outgoing messages drops them to a single email
    address.
    """
    pass


class LogOnlySMTPBackend(LogOnlyBackendMixin, SMTPBackend):
    """
    This backend intercepts outgoing messages and logs them, allowing
    only messages destined for ADMINS to be sent via SMTP.
    """
    pass
