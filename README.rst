Django-Email-Bandit
==============================

A Django email backend for hijacking email sending in test environment. It extends
the default SMTP backend to intercept outgoing emails and instead send them
to a single email address.

It does not intercept emails going to the site admins (as defined by the ADMINS
setting) so it will not impact the 500 error emails.


Requirements
-------------------------------

- Django >= 1.2


Installation
-------------------------------

To install django-email-bandit via pip::

    pip install django-email-bandit

Or you can from the latest version from Github manually::

    git clone git://github.com/caktus/django-email-bandit.git
    cd django-email-bandit
    python setup.py install

or via pip::

    pip install -e git+https://github.com/caktus/django-email-bandit.git

Add django-email-bandit to your installed apps::

    INSTALLED_APPS = (
        ...
        'bandit',
        ...
    )

For your test environment you should enable the backend::

    EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'

and set the email which will receive all of the emails::

    BANDIT_EMAIL = 'bandit@example.com'


Using django-seacucumber
-------------------------------

django-email-bandit supports sending email through SES via 
`django-seacucumber <https://github.com/duointeractive/sea-cucumber>`_.

To configure django-email-bandit, set your email backend as follows::

    EMAIL_BACKEND = 'bandit.backends.seacuke.HijackSESBackend'


Hijacking Arbitrary Backends
-------------------------------

You can also hijack email to an arbitrary Django email backend by wrapping a
backend of your choice with the HijackBackendMixin.  For example, if you wanted
to send email through SES but prefer to use 
`django-ses <https://github.com/hmarr/django-ses>`_, you would create a
class like this inside your project::

    from django_ses import SESBackend
    from bandit.backends.base import HijackBackendMixin


    class MyHijackBackend(HijackBackendMixin, SESBackend):
        """
        This backend intercepts outgoing messages drops them to a single email
        address, using the SESBackend in django-ses.
        """
        pass

and then set ``EMAIL_BACKEND`` as follows::

    EMAIL_BACKEND = 'my.project.path.to.MyHijackBackend'

Note that the order in which you specify the mixin and base class is very
important.  If you specify the mixin last, your email will not be hijacked.


Questions or Issues?
-------------------------------

If you have questions, issues or requests for improvements please let us know on
`Github <https://github.com/caktus/django-email-bandit/issues>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
