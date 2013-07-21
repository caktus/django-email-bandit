Django-Email-Bandit
==============================

A Django email backend for hijacking email sending in a staging/test environment. It extends
the default SMTP backend to intercept outgoing emails and instead send them
to a single email address. It does not intercept emails going to the site admins
(as defined by the ``ADMINS`` setting) so it will not impact the 500 error emails.

You can also configure the hijacked emails to be logged through standard Python
logging. Mixin classes are provided to use the same hijack logic for any existing
email backend such as `django-ses <https://github.com/hmarr/django-ses>`_.


Requirements
-------------------------------

- Django >= 1.2


Installation
-------------------------------

To install django-email-bandit via pip::

    pip install django-email-bandit

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


Documentation
-------------------------------

For additional documentation on configuring and using django-email-bandit you
can consult the full project documentation on `Read the Docs <https://django-email-bandit.readthedocs.org/>`_.


Questions or Issues?
-------------------------------

If you have questions, issues or requests for improvements please let us know on
`Github <https://github.com/caktus/django-email-bandit/issues>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
