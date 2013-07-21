Django-Email-Bandit Changes
==============================

History of releases and changes to the django-email-bandit project.


v1.0
-------------------------------

- Python 3 support
- Tox support for running tests with Travis CI integration
- Full project documentation
- Added ``BANDIT_WHITELIST`` setting to allow additional emails to pass through
- *Backwards incompatible* Dropped Django 1.2 support


v0.3.0
-------------------------------

- Added mixin classes for logging hijacked emails rather than sending


v0.2.0
-------------------------------

- Added support for hijacking django-seacucumber backend
- Added mixin to help with the creation of additional hijacked backends


v0.1.0
-------------------------------

- Initial public release
