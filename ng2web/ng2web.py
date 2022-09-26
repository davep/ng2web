"""Core code."""

##############################################################################
# Python imports.
import argparse
from pathlib import Path
from typing  import Optional, Union, List

##############################################################################
# Third party imports.
from ngdb import (
    __version__ as ngdb_ver, NortonGuide, Entry, MarkupText, make_dos_like
)
from jinja2 import (
    __version__ as jinja_version,
    Environment, PackageLoader, select_autoescape
)
from markupsafe import Markup, escape

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
# Locate a file within the user-specified output location.
def output( args: argparse.Namespace, file_name: Union[ Path, str ] ) -> Path:
    """Expand a file's name so that it's within the output location.

    :param ~argparse.Namespace args: The command line arguments.
    :param Union[~pathlib.Path,str] file_name: The file's name.
    :returns: The full path to the file, within the output location.
    :rtype: ~pathlib.Path


    Note that this function will expand any user information within the
    specified output path and also resolve the result.
    """
    return Path( args.output ).expanduser().resolve() / Path( file_name )

##############################################################################
# Parse the arguments.
def get_args() -> argparse.Namespace:
    """Get the arguments passed by the user.

    :returns: The parsed arguments.
    :rtype: ~argparse.Namespace
    """

    # Version information, used in a couple of paces.
    version = f"v{__version__} (ngdb v{ngdb_ver}; Jinja2 v{jinja_version})"

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
# Generate the path to the about page.
def about( guide: NortonGuide, args: argparse.Namespace ) -> Path:
    """Get the name of the about page for the guide.

    :param NortonGuide guide: The guide to generate the about name for.
    :param ~argparse.Namespace args: The command line arguments.
    :returns: The path to the about file for the guide.
    :rtype: ~pathlib.Path
    """
    return output( args, prefix( "about.html", guide ) )

##############################################################################
# Write the about page for the guide.
def write_about( guide: NortonGuide, args: argparse.Namespace, env: Environment ) -> None:
    """Write the about page for the guide.

    :param NortonGuide guide: The guide to generate the about name for.
    :param ~argparse.Namespace args: The command line arguments.
    :param Environment env: The template environment.
    """
    log( f"Writing about into {about( guide, args )}" )
    with about( guide, args ).open( "w" ) as target:
        target.write( env.get_template( "about.html" ).render() )

##############################################################################
# Generate the path to the stylesheet.
def css( guide: NortonGuide, args: argparse.Namespace ) -> Path:
    """Get the name of the stylesheet for the guide.

    :param NortonGuide guide: The guide to generate the css name for.
    :param ~argparse.Namespace args: The command line arguments.
    :returns: The path to the stylesheet for the guide.
    :rtype: ~pathlib.Path
    """
    return output( args, prefix( "style.css", guide ) )

##############################################################################
# Write the stylesheet for the guide.
def write_css( guide: NortonGuide, args: argparse.Namespace, env: Environment ) -> None:
    """Write the stylesheet for the guide.

    :param NortonGuide guide: The guide to generate the stylesheet for.
    :param ~argparse.Namespace args: The command line arguments.
    :param Environment env: The template environment.
    """
    log( f"Writing stylesheet into {css( guide, args )}" )
    with css( guide, args ).open( "w" ) as target:
        target.write( env.get_template( "base.css" ).render(
            colours = enumerate( (
                "black",
                "navy",
                "green",
                "teal",
                "maroon",
                "purple",
                "olive",
                "silver",
                "gray",
                "blue",
                "lime",
                "aqua",
                "red",
                "fuchsia",
                "yellow",
                "white"
            ) )
        ) )

##############################################################################
# Generate the name of a file for an entry in the guide.
def entry_file( guide: NortonGuide,
           args: argparse.Namespace, location: Union[ int, Entry ] ) -> Path:
    """Get the name of an entry in the guide.

    :param NortonGuide guide: The guide to generate the entry file name for.
    :param ~argparse.Namespace args: The command line arguments.
    :param Union[int,ngdb.Entry] location: The location of the entry.
    :returns: The path to the entry file name for the guide.
    :rtype: ~pathlib.Path
    """
    return output(
        args,
        prefix( f"{ location if isinstance( location, int ) else location.offset }.html", guide )
    )

##############################################################################
# Write a file for the given entry.
def write_entry( entry: Entry,
                 guide: NortonGuide, args: argparse.Namespace, env: Environment ) -> None:
    """Write the an entry from the guide.

    :param ~ngdb.Entry entry: The entry to write.
    :param NortonGuide guide: The guide the entry came from.
    :param ~argparse.Namespace args: The command line arguments.
    :param Environment env: The template environment.
    """
    log( f"Writing {entry.__class__.__name__.lower()} entry to {entry_file( guide, args, entry )}" )
    with entry_file( guide, args, entry ).open( "w" ) as target:
        target.write(
            env.get_template( f"{entry.__class__.__name__.lower()}.html" ).render(
                entry        = entry,
                previous_url = entry_file(
                    guide, args, entry.previous
                ).name if entry.has_previous else None,
                next_url     = entry_file(
                    guide, args, entry.next
                ) if entry.has_next else None,
                up_url       = entry_file(
                    guide, args, entry.parent.offset
                ).name if entry.parent else None
            )
        )

##############################################################################
# NG->HTML conversion parser.
class ToHTML( MarkupText ):
    """Class to convert some Norton Guide source into HTML"""

    def open_markup( self, cls: str ) -> str:
        """Open markup for the given class.

        :param str cls: The class of thing to open the markup for.
        :returns: The opening markup text.
        :rtype: str
        """
        return f'<span class="{cls}">'

    def close_markup( self, cls: str ) -> str:
        """Close markup for the given class.

        :param str cls: The class of thing to close the markup for.
        :returns: The closing markup text.
        :rtype: str
        """
        del cls
        return "</span>"

    def text( self, text: str ) -> None:
        """Handle the given text.

        :param str text: The text to handle.
        """
        super().text( str( escape( make_dos_like( text ) ) ) )

    def colour( self, colour: int ) -> None:
        """Handle the given colour value.

        :param int colour: The colour value to handle.
        """
        self.begin_markup( f"fg{ colour & 0xF} bg{ colour >> 4}" )

    def bold( self ) -> None:
        """Handle being asked to go to bold mode."""
        self.begin_markup( "ngb" )

    def unbold( self ) -> None:
        """Handle being asked to go out of bold mode."""
        self.end_markup()

    def reverse( self ) -> None:
        """Handle being asked to go to reverse mode."""
        self.begin_markup( "ngr" )

    def unreverse( self ) -> None:
        """Handle being asked to go out of reverse mode."""
        self.end_markup()

    def underline( self ) -> None:
        """Handle being asked to go in underline mode."""
        self.begin_markup( "ngu" )

    def ununderline( self ) -> None:
        """Handle being asked to go out of underline mode."""
        self.end_markup()

##############################################################################
# Get a title for the current page.
def page_title( guide: NortonGuide, entry: Optional[ Entry ]=None ) -> str:
    """Generate a title appropriate for the current page.

    :param NortonGuide guide: The guide that the entry came from.
    :param Optional[ngdb.Entry] entry: The entry to get the title for.
    :returns: A title for the current page.
    :rtype: str
    """

    # Start with the guide title.
    title = [ guide.title ]

    # If there's a parent menu...
    if entry and entry.parent.has_menu:
        title += [ guide.menus[ entry.parent.menu ].title ]

    # If there's a parent menu prompt...
    if entry and entry.parent.has_prompt:
        title += [ guide.menus[ entry.parent.menu ].prompts[ entry.parent.prompt ] ]

    # Join it all up.
    return " » ".join( make_dos_like( part ) for part in title )

##############################################################################
# Convert a guide to HTML.
def to_html( args: argparse.Namespace ) -> None:
    """Convert a Norton Guide into HTML.

    :param ~argparse.Namespace args: The command line arguments.
    """

    # Open the guide. Note that we turn it into a Path, and just to be kind
    # to folk, we attempt to expand any sort of ~ inside it first.
    with NortonGuide( Path( args.guide ).expanduser().resolve() ) as guide:

        # Log some basics.
        log( f"Guide: {guide.path}" )
        log( f"Output prefix: {prefix( '', guide )}" )

        # Bootstrap the template stuff.
        env = Environment(
            loader     = PackageLoader( Path( __file__ ).stem ),
            autoescape = select_autoescape()
        )

        # Set up the global variables for template expansion.
        env.globals = dict(
            generator  = f"ng2web v{__version__} (ngdb v{ngdb_ver})",
            guide      = guide,
            about_url  = about( guide, args ).name,
            stylesheet = css( guide, args ).name
        )

        # Set up the filters for the guide templates.
        env.filters = dict(
            urlify = lambda option: entry_file( guide, args, option.offset ).name,
            toHTML = lambda src: Markup( ToHTML( src ) ),
            title  = lambda entry: page_title( guide, entry )
        )

        # Write the stylesheet.
        write_css( guide, args, env )

        # Write the about page.
        write_about( guide, args, env )

        # Now, for every entry in the guide...
        for entry in guide:
            write_entry( entry, guide, args, env )

##############################################################################
# Main entry point for the tool.
def main() -> None:
    """Main entry point for the tool."""
    to_html( get_args() )

### ng2web.py ends here
