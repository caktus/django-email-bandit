from operator import and_

from django.conf import settings
from django.template.loader import render_to_string


class HijackBackendMixin(object):
    """
    This backend mixin intercepts outgoing messages drops them to a single
    email address.
    """

    def send_messages(self, email_messages):
        admins = getattr(settings, 'ADMINS', ())
        server_email = getattr(settings, 'SERVER_EMAIL', 'root@localhost')
        bandit_email = getattr(settings, 'BANDIT_EMAIL', server_email)
        approved_emails = set([server_email, bandit_email, ] + [email for name, email in admins])
        for message in email_messages:
            all_approved = reduce(and_, map(lambda e: e in approved_emails, message.to))
            if not all_approved:            
                old_to = message.to
                context = {'previous_recipients': old_to}
                header = render_to_string("bandit/hijacked-email-header.txt", context)
                message.body = header + message.body
                message.to = [bandit_email, ]
        return super(HijackBackendMixin, self).send_messages(email_messages)

