[![Actions Status](https://github.com/lyz-code/airss/workflows/Tests/badge.svg)](https://github.com/lyz-code/airss/actions)
[![Actions Status](https://github.com/lyz-code/airss/workflows/Build/badge.svg)](https://github.com/lyz-code/airss/actions)
[![Coverage Status](https://coveralls.io/repos/github/lyz-code/airss/badge.svg?branch=master)](https://coveralls.io/github/lyz-code/airss?branch=master)

Intelligent self-hosted content browser

Expected features:

* Own and control all the browsing data.
* Share only what you want with whom you want.
* Benefit from the data mining of their data to get a better browsing
    experience or discovering new content.
* Reduce the user browsing fingerprint.

# Installing

```bash
pip install airss
```

# A Simple Example

```python
{! examples/simple-example.py !} # noqa
```

# References

As most open sourced programs, `airss` is standing on the shoulders of
giants, namely:

[Pytest](https://docs.pytest.org/en/latest)
: Testing framework, enhanced by the awesome
    [pytest-cases](https://smarie.github.io/python-pytest-cases/) library that made
    the parametrization of the tests a lovely experience.

[Mypy](https://mypy.readthedocs.io/en/stable/)
: Python static type checker.

[Flakehell](https://github.com/life4/flakehell)
: Python linter with [lots of
    checks](https://lyz-code.github.io/blue-book/devops/flakehell/#plugins).

[Black](https://black.readthedocs.io/en/stable/)
: Python formatter to keep a nice style without effort.

[Autoimport](https://github.com/lyz-code/autoimport)
: Python formatter to automatically fix wrong import statements.

[isort](https://github.com/timothycrosley/isort)
: Python formatter to order the import statements.

[Pip-tools](https://github.com/jazzband/pip-tools)
: Command line tool to manage the dependencies.

[Mkdocs](https://www.mkdocs.org/)
: To build this documentation site, with the
[Material theme](https://squidfunk.github.io/mkdocs-material).

[Safety](https://github.com/pyupio/safety)
: To check the installed dependencies for known security vulnerabilities.

[Bandit](https://bandit.readthedocs.io/en/latest/)
: To finds common security issues in Python code.

[Yamlfix](https://github.com/lyz-code/yamlfix)
: YAML fixer.

# Contributing

For guidance on setting up a development environment, and how to make
a contribution to *airss*, see [Contributing to
airss](https://lyz-code.github.io/airss/contributing).
