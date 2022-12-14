talbot
======

|pypi| |docs| |ghactions| |coverage| |black|

Talbot is a library to convert scholarly metadata, modelled after the `briard ruby gem <https://github.com/front-matter/briard>`_.

`talbot` includes three modules you can import as needed (or
import all):

`Crossref` - Crossref search API. The `Crossref` module includes methods matching Crossref API routes, and a few convenience methods for getting DOI agency and random DOIs:

- `works` - `/works` route
- `members` - `/members` route
- `prefixes` - `/prefixes` route
- `funders` - `/funders` route
- `journals` - `/journals` route
- `types` - `/types` route
- `licenses` - `/licenses` route
- `registration_agency` - get DOI minting agency
- `random_dois` - get random set of DOIs

`counts` - citation counts. Includes the single `citation_count` method

`cn` - content negotiation. Includes the methods:

- `content_negotiation` - get citations in a variety of formats
- `csl_styles` - get CSL styles, used in `content_negotation` method

`WorksContainer` - A class for handling Crossref works. Pass output of works from methods on the `Crossref` class to more easily extract specific fields of works. 

Note about searching:

You are using the Crossref search API described at https://api.crossref.org/swagger-ui/index.html. When you search with query terms, on Crossref servers they are not searching full text, or even abstracts of articles, but only what is available in the data that is returned to you. That is, they search article titles, authors, etc. For some discussion on this, see https://gitlab.com/crossref/issues/-/issues/101

Rate limits
-----------

See the headers `X-Rate-Limit-Limit` and `X-Rate-Limit-Interval` for current rate limits.

The Polite Pool
---------------

To get in the polite pool it's a good idea now to include a `mailto` email
address. See docs for more information.


Installation
============

Stable version

.. code-block:: console

  pip (or pip3) install talbot

Dev version

.. code-block:: console

    pip install git+https://github.com/front-matter/talbot.git#egg=talbot


Or build it yourself locally

.. code-block:: console

    git clone https://github.com/front-matter/talbot.git
    cd Talbot
    make install

Usage
=====

Initialize a client

.. code-block:: python

    from talbot import Crossref
    cr = Crossref()

Works route

.. code-block:: python
  
  # query
  x = cr.works(query = "ecology")
  x['message']
  x['message']['total-results']
  x['message']['items']

  # fetch data by DOI
  cr.works(ids = '10.1371/journal.pone.0033693')

Members route

.. code-block:: python
  
  # ids here is the Crossref Member ID; 98 = Hindawi
  cr.members(ids = 98, works = True)

Citation counts

.. code-block:: python

  from talbot import counts
  counts.citation_count(doi = "10.1016/j.fbr.2012.01.001")

Content negotiation - get citations in many formats

.. code-block:: python

  from talbot import cn
  cn.content_negotiation(ids = '10.1126/science.169.3946.635')
  cn.content_negotiation(ids = '10.1126/science.169.3946.635', format = "citeproc-json")
  cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "rdf-xml")
  cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text")
  cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "text", style = "apa")
  cn.content_negotiation(ids = "10.1126/science.169.3946.635", format = "bibentry")

Meta
====

* Please note that this project is released with a `Contributor Code of Conduct <https://github.com/front-matter/talbot/blob/main/CODE_OF_CONDUCT.md>`__. By participating in this project you agree to abide by its terms.
* License: MIT; see `LICENSE file <https://github.com/front-matter/talbot/blob/main/LICENSE>`__

.. |pypi| image:: https://badge.fury.io/py/talbot.svg
    :target: https://badge.fury.io/py/talbot

.. |docs| image:: https://readthedocs.org/projects/talbot/badge/?version=latest
   :target: http://talbot.rtfd.org/

.. |ghactions| image:: https://github.com/front-matter/talbot/workflows/Python/badge.svg
   :target: https://github.com/front-matter/talbot/actions?query=workflow%3APython

.. |coverage| image:: https://codecov.io/gh/front-matter/talbot/branch/main/graph/badge.svg?token=6RrgNAuQmR
   :target: https://codecov.io/gh/front-matter/talbot

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
