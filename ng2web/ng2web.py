"""Core code."""

##############################################################################
# Python imports.
import argparse
from pathlib import Path

##############################################################################
# Third party imports.
from ngdb import __version__ as ngdb_ver

##############################################################################
# Local imports.
from . import __version__

##############################################################################
# Parse the arguments.
def get_args() -> argparse.Namespace:
    """Get the arguments passed by the user.

    :returns: The parsed arguments.
    :rtype: ~argparse.Namespace
    """

    # Version information, used in a couple of paces.
    version = f"v{__version__} (ngdb v{ngdb_ver})"

    # Create the argument parser object.
    parser = argparse.ArgumentParser(
        prog        = Path( __file__ ).stem,
        description = "Convert a Norton Guide database to HTML documents.",
        epilog      = version
    )

    # Add an optional output directory.
    parser.add_argument(
        "-o", "--output",
        help    = "Directory where the output files will be created.",
        default = "."
    )

    # Add --version
    parser.add_argument(
        "-v", "--version",
        help    = "Show version information.",
        action  = "version",
        version = f"%(prog)s {version}"
    )

    # The remainder is the path to the guides to look at.
    parser.add_argument( "guide", help="The guide to convert" )

    # Parse the command line.
    return parser.parse_args()

##############################################################################
# Main entry point for the tool.
def main() -> None:
    """Main entry point for the tool."""

    # Get the arguments.
    args = get_args()

    print( f"I'd convert {args.guide} in {args.output}" )

### ng2web.py ends here
