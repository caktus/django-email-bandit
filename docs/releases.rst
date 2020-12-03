Django-Email-Bandit Changes
==============================

History of releases and changes to the django-email-bandit project. This project
has reached a stable point in its development and new releases are primarily to
ensure compatibility with newer versions of Django and Python.


Supported Django Versions
-------------------------------

django-email-bandit aims to support the current security-supported releases of Django. That
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


v1.6 (released 2020-12-03)
--------------------------

- Add BANDIT_REGEXP_WHITELIST to allow match emails by regexps (#29)


v1.5 (released 2018-01-11)
--------------------------

- Added documentation regarding context variables available in the email template (#25)
- Allow BANDIT_EMAIL to be a list of addresses (#26)
- Add flake8 and coverage tox environments


v1.4 (released 2017-12-08)
--------------------------

- Added support for Django 2.0 and Python 3.5
- Dropped support for Django 1.5, 1.6, 1.7, 1.9 and Python 3.4
- Documentation improvements
- Support more email address formats (#19)


v1.3 (released 2017-10-31)
--------------------------

- Added support and test coverage for Django 1.11
- Added support and test coverage for Python 3.6
- Dropped support for Python 2.6 and Python 3.3.


v1.2 (Released 2016-11-08)
-------------------------------

- Added support and test coverage for Django 1.10


v1.1 (Released 2016-01-20)
-------------------------------

- Backends now intercept the CC and BCC fields as well
- Entire domains can be whitelisted. See the :doc:`settings documentation <settings>`.

v1.0 (Released 2014-03-21)
-------------------------------

- Python 3 support
- Tox support for running tests with Travis CI integration
- Full project documentation
- Added ``BANDIT_WHITELIST`` setting to allow specified emails to pass through
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
