from seacucumber.backend import SESBackend

from bandit.backends.base import HijackBackendMixin, LogOnlyBackendMixin


class HijackSESBackend(HijackBackendMixin, SESBackend):
    """
    This backend intercepts outgoing messages drops them to a single email
    address, using the SESBackend in django-seacucumber.
    """

    pass


class LogOnlySESBackend(LogOnlyBackendMixin, SESBackend):
    """
    This backend intercepts outgoing messages and logs them, allowing
    only messages destined for ADMINS to be sent via SES.
    """

    pass
