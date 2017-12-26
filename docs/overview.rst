Getting Started
==============================

django-email-bandit provides additional email backends for Django which reroute
outgoing emails to another email address, typically a shared inbox or group email.
Included in the intercepted message body is a list of the original recipients.
This allows you to test functionality on your site which might otherwise send
out emails to your users. Additionally, it allows recipient emails to be
white-listed so that they are sent without modification
to the original recipient(s). By default, django-email-bandit will not intercept
emails to ``ADMINS``, meaning that it will not interfere with the standard 500 error
emails provided by Django.


Installing
------------------------------

The recommended method for installing django-email-bandit is using
`pip <http://pip-installer.org>`_::

    pip install django-email-bandit

The rest of this guide assumes that you have installed the latest stable
version via pip.


Necessary Settings
------------------------------

Configure the following settings in your
project ``settings.py``. Add ``bandit`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        # Other installed apps included here
        'bandit',
    )

This is required to auto-discover the templates included with the application. To
begin intercepting emails, change your ``EMAIL_BACKEND`` setting
to one of the included backends. ``bandit.backends.smtp.HijackSMTPBackend`` is
used to change the behavior of the default ``SMTPBackend`` backend::

    EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'

Finally you should set ``BANDIT_EMAIL`` to a valid email address where you will
receive the emails which are intercepted::

    BANDIT_EMAIL = 'bandit@example.com'


Customizing the Template
------------------------------

An optional step is to customize the templates used when an email is intercepted.
The hijacked message body will contain a header defined by the ``bandit/hijacked-email-header.txt``
template. This template is given the context::

    {
        'message': message,  # Original EmailMessage object,
        'previous_recipients': previous_recipients,  # List of the original recipients
        'previous_cc': previous_cc,  # List of the original CC'ed recipients
        'previous_bcc': previous_bcc,  # List of the original BCC'ed recipients
    }

Note that the default header template doesn't include ``previous_cc`` or ``previous_bcc``, so
you'll need to create a custom template if you need those displayed.
