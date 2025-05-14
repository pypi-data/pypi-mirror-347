.. -*- coding: utf-8 -*-

Changes
-------

2.2 (2025-05-13)
~~~~~~~~~~~~~~~~

* Minor tweaks to development environment


2.2.dev2 (2025-03-08)
~~~~~~~~~~~~~~~~~~~~~

* Renew development environment:

  - modernized packaging using pdm-backend__
  - use bump-my-version__

  __ https://pypi.org/project/pdm-backend/
  __ https://pypi.org/project/bump-my-version/


2.2.dev1 (2022-12-16)
~~~~~~~~~~~~~~~~~~~~~

* Fix logging usage thru ``BuildEnvironment``, deprecated loooong ago


2.2.dev0 (2022-07-23)
~~~~~~~~~~~~~~~~~~~~~

* Drop support for Python 2

* Remove deprecated option, to support Sphinx 5

* Renew development environment:

  - modernized packaging using `PEP 517`__ and pdm-pep517__
  - replaced tox__ with nix__
  - replaced bump_version__ with bump2version__
  - replaced make with just__

  __ https://peps.python.org/pep-0517/
  __ https://pypi.org/project/pdm-pep517/
  __ https://tox.wiki/en/latest/
  __ https://nixos.org/guides/how-nix-works.html
  __ https://pypi.org/project/metapensiero.tool.bump_version/
  __ https://pypi.org/project/bump2version/
  __ https://just.systems/


2.1 (2019-03-31)
~~~~~~~~~~~~~~~~

* Minor tweak for compatibility with recently released Sphinx 2.0


2.0 (2018-06-16)
~~~~~~~~~~~~~~~~

.. important:: Given that the PostgreSQL-specific prettifier has been renamed from ``pg_query``
               to ``pglast``, I opted to reflect the fact on the value of the
               ``autodoc_sa_prettifier`` option: if you were using that tool, you must change
               it to ``pglast``.

               Sorry for the inconvenience.


1.7 (2018-05-24)
~~~~~~~~~~~~~~~~

* Avoid prettification of ``BindParameters``


1.6 (2018-05-23)
~~~~~~~~~~~~~~~~

* Use Sphinx 1.7+ API to install the extension


1.5 (2017-08-10)
~~~~~~~~~~~~~~~~

* New option ``autodoc_sa_prettifier_options`` to pass arbitrary keyword options to the
  prettifier function


1.4 (2017-08-09)
~~~~~~~~~~~~~~~~

* Replace the dynamic argument placeholders injected by SA with their literal values, leaving
  the developer's explicit bindparams alone


1.3 (2017-08-08)
~~~~~~~~~~~~~~~~

* Handle also the `pglast`__ SQL prettifier

* New options, ``autodoc_sa_prettifier`` and ``autodoc_pygments_lang``

__ https://pypi.org/project/pglast


1.2 (2017-03-22)
~~~~~~~~~~~~~~~~

* Minor tweak, no externally visible changes


1.1 (2017-01-17)
~~~~~~~~~~~~~~~~

* First release on PyPI


1.0 (unreleased)
~~~~~~~~~~~~~~~~

* Polished, tested and extended to support class' attributes as well

* Extracted from metapensiero.sphinx.patchdb
