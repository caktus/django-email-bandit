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
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'bandit',
        ),
        SITE_ID=1,
        ADMINS=(('Admin', 'admin@example.com'), ),
        BANDIT_EMAIL='bandit@example.com',
        BASE_DIR='',  # tells compatibility checker not to emit warning
    )


def runtests():
    if django.VERSION > (1, 7):
        # http://django.readthedocs.org/en/latest/releases/1.7.html#standalone-scripts
        django.setup()
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['bandit', ])
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
