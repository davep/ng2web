"""ng2web -- Norton Guide to HTML conversion tool."""

##############################################################################
# Python imports.
from importlib.metadata import version

######################################################################
# Main library information.
__author__ = "Dave Pearson"
__copyright__ = "Copyright 2021-2025, Dave Pearson"
__credits__ = ["Dave Pearson"]
__maintainer__ = "Dave Pearson"
__email__ = "davep@davep.org"
__version__ = version("ng2web")
__licence__ = "GPLv3+"


##############################################################################
# Local imports.
from .ng2web import main

##############################################################################
# Exports.
__all__ = ["main"]

### __init__.py ends here
