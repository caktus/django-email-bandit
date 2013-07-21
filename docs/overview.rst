Getting Started
==============================

Below is a guide for getting started with django-email-bandit.


How It Works
------------------------------

django-email-bandit provides additional email backends for Django which reroute
outgoing emails to another email addres, typically a shared inbox or group email. 
Included in the intercepted message body is a list of the original recipients. 
This allows you to test functionality on your site which might otherwise send 
out emails to your users. Additionally it allows recipient emails to be 
white-listed so that they are sent without modification
to the original recipient(s). By default django-email-bandit will allow the emails
in the ``ADMINS`` through meaning that it will not impact the standard 500 error
emails provided by Django.


Installing
------------------------------

The recommended method for installing django-email-bandit is using
`pip <http://pip-installer.org>`_.

    pip install django-email-bandit

The rest of this guide assumes that you have installed the latest stable
version via pip.


Necessary Settings
------------------------------

Once installed you will need to configure the following settings in your
project ``settings.py``. ``bandit`` should be included in your ``INSTALLED_APPS``.

.. code-block::python

    INSTALLED_APPS = (
        # Other installed apps included here
        'bandit',
    )

This is required to auto-discover the templates included with the application. To
enable for your test environment you need to change your ``EMAIL_BACKEND`` setting
to one of the included backends. ``bandit.backends.smtp.HijackSMTPBackend`` is
used to change the behavior of the default ``SMTPBackend`` backend.

.. code-block::python

    EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'

Finally you should set ``BANDIT_EMAIL`` to a valid email address when you will
check and view the emails which are intercepted.

.. code-block::python

    BANDIT_EMAIL = 'bandit@example.com'


Customizing the Template
------------------------------

An optional step is to customize the templates used when an email is intercepted.
The hijacked message body will contain a header define by the ``bandit/hijacked-email-header.txt``
template. This template is given the context

.. code-block::python

    {
        'message': message, # Original EmailMessage object,
        'previous_recipients': previous_recipients, # List of the original recipients
    }
