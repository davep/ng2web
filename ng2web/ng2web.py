"""Core code."""

##############################################################################
# Python imports.
import argparse
from pathlib import Path

##############################################################################
# Third party imports.
from ngdb import __version__ as ngdb_ver, NortonGuide

##############################################################################
# Local imports.
from . import __version__

##############################################################################
# Quick and dirty logger.
def log( msg: str ) -> None:
    """Simple logging function.

    :param str msg: The message to log.

    At some point soon I'll possibly switch to proper logging, but just for
    now...
    """
    print( msg )

##############################################################################
# Prefix some text with a guide's "namespace".
def prefix( text: str, guide: NortonGuide ) -> str:
    """Prefix the given text with the guide's namespace.

    :param str text: The text to prefix.
    :param NortonGuide guide: The guide we're working with.
    :returns: The prefixed text.
    :rtype: str
    """
    return f"{guide.path.stem}-{text}"

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
# Convert a guide to HTML.
def to_html( args: argparse.Namespace ) -> None:
    """Convert a Norton Guide into HTML.

    :param ~argparse.Namespace args: The command line arguments.
    """

    # Open the guide. Note that we turn it into a Path, and just to be kind
    # to folk, we attempt to expand any sort of ~ inside it first.
    with NortonGuide( Path( args.guide ).expanduser().resolve() ) as guide:
        log( f"Guide: {guide.path}" )
        log( f"Output prefix: {prefix( '', guide )}" )

##############################################################################
# Main entry point for the tool.
def main() -> None:
    """Main entry point for the tool."""
    to_html( get_args() )

### ng2web.py ends here
