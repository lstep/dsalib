from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

import dsalib

setup(name="DsaLib",
      version=dsalib.__version__,
      author = "Adelux",
      author_email = "luc stepniewski at adelux.fr",
      download_url = "http://code.google.com/p/dsalib/",
      license = "GPL",
      keywords = "debian deb linux dsa security dpkg alert",
      description = "Python module to retrieve the Debian Security Alerts (DSA) and parse them.",
      long_description = """
dsalib is a module for Python that retrieves all the details for each Debian alert (DSA) published on Debian's security website (http://security.debian.org/ ), parses it, and put it in an exploitable/queryable way. This module has been created for use with the project dsacheck.
Please note that this module uses decorators, so you'll need at least Python 2.4.""",

      url = "http://code.google.com/p/dsalib/",
      zip_safe = True,
      packages = find_packages(exclude=['tests','ez_setup']),
      package_data = {
        # Include all that is in data/
        'dsalib' : ['data/*.txt'],
      },

      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],

      test_suite = "dsalib.tests.test_all.suite",
      )
