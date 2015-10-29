from __future__ import unicode_literals

import logging

from functools import reduce
from operator import and_

from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger('bandit.backends.base')


class HijackBackendMixin(object):
    """
    This backend mixin intercepts outgoing messages drops them to a single
    email address.
    """

    def __init__(self, *args, **kwargs):
        self.log_only = kwargs.pop('log_only', False)
        self.log_level = kwargs.pop('log_level', logging.DEBUG)
        super(HijackBackendMixin, self).__init__(*args, **kwargs)

    def send_messages(self, email_messages):
        admins = getattr(settings, 'ADMINS', ())
        server_email = getattr(settings, 'SERVER_EMAIL', 'root@localhost')
        bandit_email = getattr(settings, 'BANDIT_EMAIL', server_email)
        whitelist_emails = set(getattr(settings, 'BANDIT_WHITELIST', ()))
        approved_emails = set([server_email, bandit_email, ] + list(whitelist_emails) +
                              [email for name, email in admins])

        def is_approved(email):
            local_part, _, domain = email.rpartition('@')
            return email in approved_emails or domain in whitelist_emails

        to_send = []
        logged_count = 0
        for message in email_messages:
            recipients = message.to + message.cc + message.bcc
            all_approved = reduce(and_, map(is_approved, recipients))
            if all_approved:
                to_send.append(message)
            else:
                context = {'message': message,
                           'previous_recipients': message.to,
                           'previous_cc': message.cc,
                           'previous_bcc': message.bcc
                           }  # included for backwards compatibility
                log_message = render_to_string("bandit/hijacked-email-log-message.txt", context)
                logger.log(self.log_level, log_message)
                if not self.log_only:
                    header = render_to_string("bandit/hijacked-email-header.txt", context)
                    message.body = header + message.body
                    message.to = [bandit_email]
                    # clear cc/bcc
                    message.cc = []
                    message.bcc = []
                    to_send.append(message)
                else:
                    # keep track of how many messages were only logged so we
                    # can report them as sent to the caller
                    logged_count += 1
        sent_count = super(HijackBackendMixin, self).send_messages(to_send) or 0
        return sent_count + logged_count


class LogOnlyBackendMixin(HijackBackendMixin):

    def __init__(self, *args, **kwargs):
        kwargs['log_only'] = True
        super(LogOnlyBackendMixin, self).__init__(*args, **kwargs)
