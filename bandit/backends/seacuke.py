from seacucumber.backend import SESBackend

from bandit.backends.base import HijackBackendMixin


class HijackSESBackend(HijackBackendMixin, SESBackend):
    """
    This backend intercepts outgoing messages drops them to a single email
    address, using the SESBackend in django-seacucumber.
    """
    pass
