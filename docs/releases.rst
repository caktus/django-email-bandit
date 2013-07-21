Django-Email-Bandit Changes
==============================

History of releases and changes to the django-email-bandit project. This project
has reached a stable point in its development and new releases are primarily to
ensure compatibility with newer versions of Django and Python.


Supported Django Versions
-------------------------------

django-email-bandit targets to support the current security supported releases of Django. That
includes the most recent version and the prior release. While we will avoid unnecessarily
dropping support for earlier releases of Django, changes in new versions which
break compatibility outside of this window will result in dropped support for that
version of Django. Any dropped Django versions will be included in the release notes.


Deprecation Policy
-------------------------------

Beginning with the 1.0 release all backwards incompatible changes will go through a two release
deprecation policy similar to Django. A feature deprecated in one version will
raise a ``PendingDeprecationWarning``. In the following release that will be raised
to a ``DeprecationWarning`` and the following release the feature and it's related compatibility
code will be removed.


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
