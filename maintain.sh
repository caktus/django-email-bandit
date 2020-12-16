#!/bin/sh
set -ex

pip install -Ur dev-requirements.txt
pre-commit install
pre-commit run -a
tox
coverage run runtests.py && coverage report
sphinx-build docs docs/_build/html
