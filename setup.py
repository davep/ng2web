"""Setup file for the ng2web tool."""

##############################################################################
# Python imports.
from pathlib    import Path
from setuptools import setup, find_packages

##############################################################################
# Import the library itself to pull details out of it.
import ng2web

##############################################################################
# Work out the location of the README file.
def readme():
    """Return the full path to the README file.

    :returns: The path to the README file.
    :rtype: ~pathlib.Path
    """
    return Path( __file__).parent.resolve() / "README.md"

##############################################################################
# Load the long description for the package.
def long_desc():
    """Load the long description of the package from the README.

    :returns: The long description.
    :rtype: str
    """
    with readme().open( "r", encoding="utf-8" ) as rtfm:
        return rtfm.read()

##############################################################################
# Perform the setup.
setup(

    name                          = "ng2web",
    version                       = ng2web.__version__,
    description                   = str( ng2web.__doc__ ),
    long_description              = long_desc(),
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/davep/ng2web",
    author                        = ng2web.__author__,
    author_email                  = ng2web.__email__,
    maintainer                    = ng2web.__maintainer__,
    maintainer_email              = ng2web.__email__,
    packages                      = find_packages(),
    package_data                  = { "ng2web": [ "py.typed", "templates/*", "templates/inc/*" ] },
    include_package_data          = True,
    install_requires              = [ "ngdb", "jinja2" ],
    python_requires               = ">=3.8",
    keywords                      = "library dbase clipper norton guide reader converter html",
    entry_points                  = {
        "console_scripts": "ng2web=ng2web.ng2web:main"
    },
    license                       = (
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ),
    classifiers                   = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
        "Typing :: Typed"
    ]

)

### setup.py ends here
