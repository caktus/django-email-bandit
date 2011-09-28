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

For your test environment you should enable the backend::

    EMAIL_BACKEND = 'bandit.backends.HijackBackend'

and set the email which will receive all of the emails::

    BANDIT_EMAIL = 'bandit@example.com'


Questions or Issues?
-------------------------------

If you have questions, issues or requests for improvements please let us know on
`Github <https://github.com/caktus/django-email-bandit/issues>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
