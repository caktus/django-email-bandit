django-email-bandit
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
    https://github.com/caktus/django-email-bandit/workflows/lint-test/badge.svg?branch=master
    :alt: Build Status
    :target: https://github.com/caktus/django-email-bandit/actions?query=branch%3Amaster

.. |develop-status| image::
    https://github.com/caktus/django-email-bandit/workflows/lint-test/badge.svg?branch=master
    :alt: Build Status
    :target: https://github.com/caktus/django-email-bandit/actions?query=branch%3Adevelop


Requirements
-------------------------------

- Python 3
- Django >= 2.2 (supported versions)


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

or even multiple addresses::

    BANDIT_EMAIL = ['bandit@example.com', 'accomplice@example.com']

It's also possible to whitelist certain email addresses and domains::

    BANDIT_WHITELIST = [
        'iloveemail@example.com',  # Just this specific email address
        'example.net'   # All email addresses @example.net
    ]


Documentation
-------------------------------

Full project documentation is on `Read the Docs <https://django-email-bandit.readthedocs.org/>`_.


Maintainer Information
-------------------------------

We use Github Actions to lint (using pre-commit, black, isort, and flake8),
test (using tox and tox-gh-actions), calculate coverage (using coverage), and build
documentation (using sphinx).

We have a local script to do these actions locally, named ``maintain.sh``::

  $ ./maintain.sh

A Github Action workflow also builds and pushes a new package to PyPI whenever a new
Release is created in Github. This uses a project-specific PyPI token, as described in
the `PyPI documentation here <https://pypi.org/help/#apitoken>`_. That token has been
saved in the ``PYPI_PASSWORD`` settings for this repo, but has not been saved anywhere
else so if it is needed for any reason, the current one should be deleted and a new one
generated.

As always, be sure to bump the version in ``bandit/__init__.py`` before creating a
Release, so that the proper version gets pushed to PyPI.


Questions or Issues?
-------------------------------

If you have questions, issues or requests for improvements please let us know on
`Github <https://github.com/caktus/django-email-bandit/issues>`_.

Development sponsored by `Caktus Consulting Group, LLC
<https://www.caktusgroup.com/services>`_.
