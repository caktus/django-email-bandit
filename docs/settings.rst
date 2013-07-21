Settings for django-email-bandit
========================================

Below are the additional settings defined and used by django-email-bandit. These
should be added and configured in your project ``settings.py``.


``BANDIT_EMAIL``
----------------------------------------

The ``BANDIT_EMAIL`` defines the email address which recieves the hijacked emails.
This defaults to the ``SERVER_EMAIL`` setting if not set.


``BANDIT_WHITELIST``
----------------------------------------

By default django-email-bandit will intercept all outgoing emails unless they
are sent to the ``SERVER_EMAIL`` or one of the emails in the ``ADMINS`` setting.
If you would like to white-list additional emails which should be allowed to
continue onto the original recipient you can add those email addresses to
``BANDIT_WHITELIST``. ``BANDIT_WHITELIST`` defaults to an empty tuple.