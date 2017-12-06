#!/usr/bin/env python
import sys

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db',
            }
        },
        MIDDLEWARE_CLASSES=(),
        INSTALLED_APPS=(
            'bandit',
        ),
        SITE_ID=1,
        ADMINS=(('Admin', 'admin@example.com'), ),
        BANDIT_EMAIL='bandit@example.com',
        BANDIT_WHITELIST=('whitelisted.test.com', ),
        BASE_DIR='',  # tells compatibility checker not to emit warning
        TEMPLATES=[
            {
                "BACKEND": 'django.template.backends.django.DjangoTemplates',
                "DIRS": ['bandit/templates'],
            }
        ],
    )


def runtests():
    django.setup()
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=True)
    failures = test_runner.run_tests(['bandit'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
