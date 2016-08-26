.. image:: https://coveralls.io/repos/Capitains/nemo-xslt2-plugin/badge.svg?service=github
  :alt: Coverage Status
  :target: https://coveralls.io/github/Capitains/nemo-xslt2-plugin
.. image:: https://travis-ci.org/Capitains/nemo-xslt2-plugin.svg
  :alt: Build Status
  :target: https://travis-ci.org/Capitains/nemo-xslt2-plugin
.. image:: https://badge.fury.io/py/nemo_xslttwo_plugin.svg
  :alt: PyPI version
  :target: http://badge.fury.io/py/nemo_xslttwo_plugin
.. image:: https://readthedocs.org/projects/docs/badge/?version=latest
    :alt: Documentation
    :target: https://nemo-xslt2-plugin.readthedocs.io/en/latest/
What ?
######

Nemo XSLT 2 Plugin is a plugin for Nemo which brings XSLT2 to Python and Nemo

Install
*******
To install it, simply do : :code:`pip3 install nemo_xslttwo_plugin` or

.. code-block:: bash

    git clone https://github.com/Capitains/nemo-xslt2-plugin.git
    cd nemo-xslt2-plugin
    python3 setup.py install

You need java to be installed on your machine as well as having downloaded the Saxon HE jar. **To run the tests** you \
will need to run "make requirements" 

From there, you will be able to call it in your python scripts this way :

.. code-block:: python
    from nemo_xslttwo_plugin import SaxonShellTransform
    from flask_nemo import Nemo
    saxon = SaxonShellTransform(
        "./jars/saxon.jar",
        "./tests/data/xsl/ciham.xsl"
    )
    nemo = Nemo(
        # ...
        transform={
            "default": saxon.transform
        }
    )
    
Licenses
########

XSLT and XML Tests files
************************

The XSLT and XML files are given graciously by PhD. Ariane Pinche (Université Lyon 3, CIHAM) and are her property.