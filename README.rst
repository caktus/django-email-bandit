Django-Email-Bandit
==============================

.. sidebar:: Build Status

   :master: |master-status|
   :develop: |develop-status|

A Django email backend for hijacking email sending in a staging/test environment. It extends
the default SMTP backend to intercept outgoing emails and instead send them
to a single email address that you specify. It does not intercept emails going to the site admins
(as defined by the ``ADMINS`` setting) so it will not interfere with 500 error emails.

You can also configure the hijacked emails to be logged through standard Python
logging. Mixin classes are provided to use the same hijack logic for any existing
email backend such as `django-ses <https://github.com/hmarr/django-ses>`_.

.. |master-status| image::
    https://api.travis-ci.org/caktus/django-email-bandit.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/caktus/django-email-bandit

.. |develop-status| image::
    https://api.travis-ci.org/caktus/django-email-bandit.svg?branch=develop
    :alt: Build Status
    :target: https://travis-ci.org/caktus/django-email-bandit


Requirements
-------------------------------

- Python 2.7 or 3.5+
- Django >= 1.8 (supported versions)


Installation
-------------------------------

To install django-email-bandit via pip::

    pip install django-email-bandit

For your test environment you should enable the backend::

    EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'

and set the email which will receive all of the emails::

    BANDIT_EMAIL = 'bandit@example.com'

It's also possible to whitelist certain email addresses and domains::

    BANDIT_WHITELIST = [
        'iloveemail@example.com',  # Just this specific email address
        'example.net'   # All email addresses @example.net
    ]


Documentation
-------------------------------

Full project documentation is on `Read the Docs <https://django-email-bandit.readthedocs.org/>`_.


Questions or Issues?
-------------------------------

If you have questions, issues or requests for improvements please let us know on
`Github <https://github.com/caktus/django-email-bandit/issues>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
