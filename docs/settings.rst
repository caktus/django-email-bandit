Settings for django-email-bandit
========================================

These should be in your project ``settings.py``.


``BANDIT_EMAIL``
----------------------------------------

The ``BANDIT_EMAIL`` defines the email address which recieves the hijacked emails.
This defaults to the ``SERVER_EMAIL`` setting if not set::

    BANDIT_EMAIL = 'bandit@example.com'


``BANDIT_WHITELIST``
----------------------------------------

By default django-email-bandit will intercept all outgoing emails unless they
are sent to the ``SERVER_EMAIL`` or one of the emails in the ``ADMINS`` setting.
If there are email addresses that should receive mail from your application normally,
add those email addresses to
``BANDIT_WHITELIST``. ``BANDIT_WHITELIST`` defaults to an empty tuple::

    BANDIT_WHITELIST = ('iloveemail@example.com', )
