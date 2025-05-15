*********
LinkMedic
*********

.. image:: https://img.shields.io/pypi/v/linkmedic
   :name: PyPI
   :target: https://pypi.org/project/linkmedic/

.. image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :name: License: 3-Clause BSD
   :target: https://opensource.org/license/BSD-3-Clause

.. image:: https://img.shields.io/badge/Python-%3E=3.9-blue
   :name: Minimum supported Python version: 3.9

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :name: Coding style: Black
   :target: https://github.com/psf/black

A Python script for checking links and resources used in local static webpages (``.htm``, ``.html``), OpenDocument files (``.odt``, ``.odp``, ``.ods``), and single OpenDocument XML files (``.fodt``, ``.fodp``, ``.fods``).

``linkmedic`` starts a test web server, requests an entry page from the server, and crawls all local pages. It checks all links within specific HTML tags (``<a>`` ``<img>`` ``<script>`` ``<link>`` ``<iframe>`` ``<event-listener>``) and reports any dead links found. If a link appears on multiple pages, it is tested only once to avoid redundant checks. By default, links to the external websites are ignored. If there is a ``.linkignore`` file in the website's root, links matching the regular expressions listed in this file (one link per line; see below for examples) are also ignored during testing. After checking all the links, if any dead links are discovered, ``linkmedic`` exits with a non-zero status code.

For testing links in dynamic HTML content (e.g., using JavaScript template engines) or other document formats, you must first convert your files (using a third-party tool) to static HTML and then run ``linkmedic``.

Quick start
###########

Install prerequisites
*********************
Depending on your operating system, you may have multiple options for installing the prerequisites:

* `Python <https://www.python.org/downloads/>`__: ``linkmedic`` is only tested on `officially supported Python versions <https://devguide.python.org/versions/>`__.
* A ``Python`` package installer: For example, `pip <https://pip.pypa.io/en/stable/installation/>`__

Install linkmedic
*****************
You can install the ``linkmedic`` using your favorite Python package installer. For example, using ``pip``, you can download it from `PyPI <https://pypi.org/project/linkmedic/>`__:

.. code-block:: shell

  pip install linkmedic


Run
***
To start a test web server with files at ``/var/www`` and crawl the pages and test all the links starting from the ``/var/www/index.html`` page, run:

.. code-block:: shell

  linkmedic --root=/var/www


Usage & Options
###############

Mirror package repository
*************************

You can also install ``linkmedic`` from the MPCDF GitLab package repository:

.. code-block:: shell

  pip install linkmedic --index-url https://gitlab.mpcdf.mpg.de/api/v4/projects/5763/packages/pypi/simple


Container
*********
You can use one of the container images, which have the required libraries and `linkmedkit <https://gitlab.mpcdf.mpg.de/tbz/linkmedkit>`_ already installed:

.. code-block:: shell

  quay.io/meisam/linkmedic:latest

.. code-block:: shell

  gitlab-registry.mpcdf.mpg.de/tbz/linkmedic:latest

You can access a specific version of ``linkmedic`` using container tags e.g. ``linkmedic:v0.7.4`` instead of ``linkmedic:latest``. See all available container tags `here <https://quay.io/repository/meisam/linkmedic?tab=tags>`_.

When using a container image, ``linkmedic``'s test web server needs to have access to the files for your website pages from inside the container. Depending on your container engine, you may need to mount the path to your files inside the container. For example, using `podman <https://podman.io/>`_:

.. code-block:: shell

  podman run --volume /www/public:/test quay.io/meisam/linkmedic:latest linkmedic --root=/test

Here, the ``--volume /www/public:/test`` flag mounts the directory ``/www/public`` inside the container at the path ``/test``.

.. _ci-cd:

CI/CD
*****
You can also use the container image in your CI/CD pipelines. For example, for GitLab CI, in the ``.gitlab-ci.yml`` file:

.. code-block:: yaml

  test_internal_links:
    image: quay.io/meisam/linkmedic:latest
    script:
      - linkmedic --root=/var/www/ --entry=index.html --warn-http --with-badge
    after_script:
      - gitlab_badge_sticker.sh


or for Woodpecker CI in the ``.woodpecker.yml`` file:

.. code-block:: yaml

  test_internal_links:
    image: quay.io/meisam/linkmedic:latest
    commands:
      - linkmedic --root=/var/www/ --entry=index.html --warn-http

If you want to check the external links of your website in your CI pipeline, you must avoid running multiple tests in a short period of time, e.g., on each commit to the development branches. Otherwise, the IP address of your CI runners may get banned by external web servers. For example, in GitLab CI, you can limit the external link checks to only the default branch of your Git repository:

.. code-block:: yaml

  test_external_links:
    image: quay.io/meisam/linkmedic:latest
    rules:
      - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    script:
      - linkmedic --root=/var/www/ --ignore-local --with-badge
    after_script:
      - gitlab_badge_sticker.sh
    allow_failure: true  

Please note that the ``gitlab_badge_sticker.sh`` script used in these examples requires an API access token ``CI_API_TOKEN`` with maintainer permission to modify the GitLab repository badges. See the `linkmedkit documentation <https://gitlab.mpcdf.mpg.de/tbz/linkmedkit>`_ for more details.

CLI reference
*************

* Display help: This will show all the command-line options and their default values.

.. code-block:: shell

  linkmedic -h

* Start the web server with the current directory as the root path of the server. Starting from ``index.html``, crawl the pages and test all the links.

.. code-block:: shell

  linkmedic

* Start the web server with ``./tests/public1/`` as the root path of the server. Starting from ``index.html``, crawl the pages and test all the links.

.. code-block:: shell

  linkmedic --root=./tests/public1/

* Start the web server with ``./tests/public1/`` as the root path of the server. Starting from ``index2.html``, crawl the pages and test all the links. The entry point should be relative to the server root. (In the example, ``index2.html`` should be accessible at ``./tests/public1/index2.html``)

.. code-block:: shell

  linkmedic --root=./tests/public1/ --entry=index2.html

* Configure the test web server not to redirect missing local pages (e.g., from ``/directory/page`` to ``/directory/page.html``).

.. code-block:: shell

  linkmedic --no-local-redirect

* Check links to external websites.
  
  [**IMPORTANT**: You must avoid running the link checker on external links multiple times in a short period, e.g., on each commit to the development branch. Otherwise, the IP address of your machine (or CI runners) may get banned by the CDN or the DoS mitigation solution of the external web servers. See the `CI/CD section <ci-cd_>`__ for a solution.]

.. code-block:: shell

  linkmedic --check-external

* Do not follow external link redirections. Depending on the configuration of external web servers, this option can result in some dead links not being detetcted when instead of returning 404 page directly, the webserver is asking the client to load another page.

.. code-block:: shell

  linkmedic --no-external-redirects

* Ignore local dead links and activates external link checking.

.. code-block:: shell

  linkmedic --ignore-local

* Do not consider external links that return HTTP status codes 403 and 503 as dead links.

.. code-block:: shell

  linkmedic --ignore-status 403 503

* Check links in an OpenDocument file (e.g., ``.odt``, ``.odp``, ``.ods``), or a single OpenDocument XML file (e.g., ``.fodt``, ``.fodp``, ``.fods``).

.. code-block:: shell

  linkmedic --entry=./presentation.odp

* Show warning for HTTP links.

.. code-block:: shell

  linkmedic --warn-http

* If any link to ``mydomain.com`` is encountered, treat it as an internal link and resolve it locally.

.. code-block:: shell

  linkmedic --domain=mydomain.com

* Start the web server on port 3000. If the web server cannot be started on the requested port, the initializer will automatically try the next available ports.

.. code-block:: shell

  linkmedic --port=3000

* Generate badge information file. Depending on the type of diagnosis, this file will be named ``badge.dead_internal_links.json``, ``badge.dead_external_links.json``, or ``badge.dead_links.json``. If the ``--warn-http`` flag is used, a badge file for the number of discovered HTTP links will also be written to the ``badge.http_links.json`` file. These files can be used to generate badges (see `linkmedkit`_ scripts) or to serve as a response for the `shields.io endpoint <https://shields.io/badges/endpoint-badge>`_.

.. code-block:: shell

  linkmedic --with-badge

* Check the links but always exit with code 0.

.. code-block:: shell

  linkmedic --exit-zero

* Log the output at a different level of verbosity. If more than one of these flags is defined, the most restrictive one will be in effect.

  -  ``--verbose`` : log debug information
  -  ``--quiet`` : log only errors
  -  ``--silent`` : completely silence the output logs

* Dump the crawler links list to the ``linkmedic.links`` file. If the ``--domain`` flag has not been set, local links will be referenced from the website root as ``/your/path/page.html``.

.. code-block:: shell

  linkmedic --dump-links

.linkignore
***********
Each line in the ``.linkignore`` file specifies a `regex pattern <https://docs.python.org/3/library/re.html#regular-expression-syntax>`_ for addresses that should be ignored during link checks. Note that regex matches ``.`` to any character (use ``\.`` for matching only to ``.``) and the leading ``/`` is considered when matching local links.

.. code-block:: shell

  /ignore/.*/this
  /invalidfile\.tar\.gz
  /will_add/later\.html
  https://not\.accessible\.com


Development
###########
This project uses `PDM <https://pdm-project.org/latest/>`_ for packaging and dependency management, `vermin <https://pypi.org/project/vermin/>`_ and `bandit <https://pypi.org/project/bandit/>`_ for validation, `black <https://pypi.org/project/black/>`_ and `isort <https://pypi.org/project/isort/>`_ for code styling, and `check-jsonschema <https://pypi.org/project/check-jsonschema/>`_ and `jq <https://jqlang.org/>`_ for testing. See the `developers guide <DEVELOPERS.rst>`_ for more details.

History
#######
The original idea for this project came from Dr. Klaus Reuter (MPCDF). Fruitful discussions with Dr. Sebastian Kehl (MPCDF) facilitated the packaging and release of this project.

Accompanying tools for ``linkmedic`` have been moved to a separate repository (`linkmedkit`_) starting with version 0.7.

License
#######
* Copyright 2021-2023 M. Farzalipour Tabriz, Max Planck Computing and Data Facility (MPCDF)
* Copyright 2023-2025 M. Farzalipour Tabriz, Max Planck Institute for Physics (MPP)

All rights reserved.

This software may be modified and distributed under the terms of the 3-Clause BSD License. See the LICENSE file for details.
