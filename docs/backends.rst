Additional Email Backends
==============================

Beyond the ``bandit.backends.smtp.HijackSMTPBackend`` used in the getting started
guide, django-email-bandit defines additional backends other uses as well as
contains helpers for hijacking already customized backends.


Using django-seacucumber
-------------------------------

django-email-bandit supports sending email through SES via 
`django-seacucumber <https://github.com/duointeractive/sea-cucumber>`_.

To configure django-email-bandit, set your email backend as follows:

.. code-block::python

    EMAIL_BACKEND = 'bandit.backends.seacuke.HijackSESBackend'


Only logging emails
-------------------

In environments where your application may generate lots of emails all at once,
it may be desirable to hijack emails to non-admins and have them logged, but
not sent out. The logging is done using the standard Python logging facilities
using the ``bandit`` logger at the ``DEBUG`` level.

django-email-bandit supports this with the ``bandit.backends.smtp.LogOnlySMTPBackend``
and the ``bandit.backends.seacuke.LogOnlySESBackend``. For example, to configure
django-email-bandit to only log emails to non-admins, but still send via SMTP
emails to admins, configure your email backend like so:

.. code-block::python

    EMAIL_BACKEND = 'bandit.backends.smtp.LogOnlySMTPBackend'

The log message which is generated can be customized by overriding the
``bandit/hijacked-email-log-message.txt`` template.


Hijacking Arbitrary Backends
-------------------------------

You can also hijack email to an arbitrary Django email backend by wrapping a
backend of your choice with the HijackBackendMixin.  For example, if you wanted
to send email through SES but prefer to use 
`django-ses <https://github.com/hmarr/django-ses>`_, you would create a
class like this inside your project:

.. code-block::python

    from django_ses import SESBackend
    from bandit.backends.base import HijackBackendMixin


    class MyHijackBackend(HijackBackendMixin, SESBackend):
        """
        This backend intercepts outgoing messages drops them to a single email
        address, using the SESBackend in django-ses.
        """
        pass

and then set ``EMAIL_BACKEND`` as follows:

.. code-block::python

    EMAIL_BACKEND = 'my.project.path.to.MyHijackBackend'

Note that the order in which you specify the mixin and base class is very
important.  If you specify the mixin last, your email will not be hijacked.