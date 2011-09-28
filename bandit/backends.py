from operator import and_

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.template.loader import render_to_string


class HijackBackend(SMTPBackend):
    """
    This backend intercepts outgoing messages drops them to a single email
    address.
    """

    def send_messages(self, email_messages):
        admins = getattr(settings, 'ADMINS', ())
        sever_email = getattr(settings, 'SERVER_EMAIL', 'root@localhost')
        bandit_email = getattr(settings, 'BANDIT_EMAIL', sever_email)
        approved_emails = set([sever_email, bandit_email, ] + [email for name, email in admins])
        for message in email_messages:
            all_approved = reduce(and_, map(lambda e: e in approved_emails, message.to))
            if not all_approved:            
                old_to = message.to
                context = {'previous_recipients': old_to}
                header = render_to_string("bandit/hijacked-email-header.txt", context)
                message.body = header + message.body
                message.to = [bandit_email, ]
        return super(HijackBackend, self).send_messages(email_messages)
