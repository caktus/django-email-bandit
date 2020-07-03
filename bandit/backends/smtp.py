from __future__ import unicode_literals

from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

from bandit.backends.base import HijackBackendMixin, LogOnlyBackendMixin


class HijackSMTPBackend(HijackBackendMixin, SMTPBackend):
    """
    This backend intercepts outgoing messages and logs them, allowing
    only messages destined for ADMINS, BANDIT_EMAIL, SERVER_EMAIL,
    BANDIT_REGEX_WHITELIST or BANDIT_WHITELIST to be sent via SMTP.

    It also sends intercepted messages to BANDIT_EMAIL.
    """
    pass


class LogOnlySMTPBackend(LogOnlyBackendMixin, SMTPBackend):
    """
    This backend intercepts outgoing messages and logs them, allowing
    only messages destined for ADMINS, BANDIT_EMAIL, SERVER_EMAIL,
    BANDIT_REGEX_WHITELIST, or BANDIT_WHITELIST to be sent via SMTP.

    It does not forward intercepted messages.
    """
    pass
