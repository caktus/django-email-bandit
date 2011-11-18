from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

from bandit.backends.base import HijackBackendMixin


class HijackSMTPBackend(HijackBackendMixin, SMTPBackend):
    """
    This backend intercepts outgoing messages drops them to a single email
    address.
    """
    pass
