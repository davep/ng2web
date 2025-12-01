"""Core code."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
import argparse
from datetime import datetime
from pathlib import Path

##############################################################################
# Jinja2 imports.
from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    select_autoescape,
)
from jinja2 import (
    __version__ as jinja_version,
)

##############################################################################
# MarkupSafe imports.
from markupsafe import Markup, escape

##############################################################################
# Third party imports.
from ngdb import Entry, MarkupText, NortonGuide, make_dos_like
from ngdb import __version__ as ngdb_ver

##############################################################################
# Local imports.
from . import __version__


##############################################################################
def log(msg: str) -> None:
    """Simple logging function.

    Args:
        msg: The message to log.

    At some point soon I'll possibly switch to proper logging, but just for
    now...
    """
    print(msg)


##############################################################################
def prefix(text: str, guide: NortonGuide) -> str:
    """Prefix the given text with the guide's namespace.

    Args:
        text: The text to prefix.
        guide: The guide we're working with.

    Returns:
        The prefixed text.
    """
    return f"{guide.path.stem}-{text}"


##############################################################################
def get_args() -> argparse.Namespace:
    """Get the arguments passed by the user.

    Returns:
        The parsed arguments.
    """

    # Version information, used in a couple of paces.
    version = f"v{__version__} (ngdb v{ngdb_ver}; Jinja2 v{jinja_version})"

    # Create the argument parser object.
    parser = argparse.ArgumentParser(
        prog=Path(__file__).stem,
        description="Convert a Norton Guide database to HTML documents",
        epilog=version,
    )

    # Add an optional switch for making an index.html.
    parser.add_argument(
        "-i",
        "--index",
        action="store_true",
        help="Generate the first entry in the guide as index.html",
    )

    # Add an optional output directory.
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Directory where the output files will be created",
        default=".",
    )

    # Add an optional source of template files.
    parser.add_argument(
        "-t",
        "--templates",
        type=Path,
        help="Directory of template overrides",
        required=False,
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s {version}",
    )

    # The remainder is the path to the guides to look at.
    parser.add_argument("guide", help="The guide to convert", type=Path)

    # Parse the command line.
    return parser.parse_args()


##############################################################################
def about(guide: NortonGuide, output_directory: Path) -> Path:
    """Get the name of the about page for the guide.

    Args:
        guide: The guide to generate the about name for.
        output_directory: The output directory.

    Returns:
        The path to the about file for the guide.
    """
    return output_directory / prefix("about.html", guide)


##############################################################################
def write_about(guide: NortonGuide, output_directory: Path, env: Environment) -> None:
    """Write the about page for the guide.

    Args:
        guide: The guide to generate the about name for.
        output_directory: The output directory.
        env: The template environment.
    """
    log(f"Writing about into {about(guide, output_directory)}")
    with about(guide, output_directory).open("w") as target:
        target.write(env.get_template("about.html").render())


##############################################################################
def css(guide: NortonGuide, output_directory: Path) -> Path:
    """Get the name of the stylesheet for the guide.

    Args:
        guide: The guide to generate the css name for.
        output_directory: The output directory.

    Returns:
        The path to the stylesheet for the guide.
    """
    return output_directory / prefix("style.css", guide)


##############################################################################
def write_css(guide: NortonGuide, output_directory: Path, env: Environment) -> None:
    """Write the stylesheet for the guide.

    Args:
        guide: The guide to generate the stylesheet for.
        output_directory: The output directory.
        env: The template environment.
    """
    log(f"Writing stylesheet into {css(guide, output_directory)}")
    with css(guide, output_directory).open("w") as target:
        target.write(
            env.get_template("base.css").render(
                colours=enumerate(
                    (
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
                        "white",
                    )
                )
            )
        )


##############################################################################
def entry_file(
    guide: NortonGuide, output_directory: Path, location: int | Entry, make_index: bool
) -> Path:
    """Get the name of an entry in the guide.

    Args:
        guid: The guide to generate the entry file name for.
        output_directory: The output directory.
        location: The location of the entry.
        make_index: Should we make the first entry `index.html`?

    Returns:
        The path to the entry file name for the guide.
    """
    if (
        offset := location if isinstance(location, int) else location.offset
    ) == guide.first_entry and make_index:
        return output_directory / "index.html"
    return output_directory / prefix(f"{offset}.html", guide)


##############################################################################
def write_entry(
    entry: Entry,
    guide: NortonGuide,
    output_directory: Path,
    make_index: bool,
    env: Environment,
) -> None:
    """Write the an entry from the guide.

    Args:
        entry: The entry to write.
        guide: The guide the entry came from.
        output_directory: The output directory.
        make_index: Make first entry be `index.html`?
        env: The template environment.
    """
    log(
        f"Writing {entry.__class__.__name__.lower()} entry to {entry_file(guide, output_directory, entry, make_index)}"
    )
    with entry_file(guide, output_directory, entry, make_index).open("w") as target:
        target.write(
            env.get_template(f"{entry.__class__.__name__.lower()}.html").render(
                entry=entry,
                previous_url=(
                    entry_file(guide, output_directory, entry.previous, make_index).name
                    if entry.has_previous
                    else None
                ),
                next_url=(
                    entry_file(guide, output_directory, entry.next, make_index).name
                    if entry.has_next
                    else None
                ),
                up_url=(
                    entry_file(
                        guide, output_directory, entry.parent.offset, make_index
                    ).name
                    if entry.parent
                    else None
                ),
            )
        )


##############################################################################
class ToHTML(MarkupText):
    """Class to convert some Norton Guide source into HTML"""

    def open_markup(self, cls: str) -> str:
        """Open markup for the given class.

        Args:
            cls: The class of thing to open the markup for.

        Returns:
            The opening markup text.
        """
        return f'<span class="{cls}">'

    def close_markup(self, cls: str) -> str:
        """Close markup for the given class.

        Args:
            cls: The class of thing to close the markup for.

        Returns:
            The closing markup text.
        """
        del cls
        return "</span>"

    def text(self, text: str) -> None:
        """Handle the given text.

        Args:
            text: The text to handle.
        """
        super().text(str(escape(make_dos_like(text))))

    def colour(self, colour: int) -> None:
        """Handle the given colour value.

        Args:
            colour: The colour value to handle.
        """
        self.begin_markup(f"fg{colour & 0xF} bg{colour >> 4}")

    def bold(self) -> None:
        """Handle being asked to go to bold mode."""
        self.begin_markup("ngb")

    def unbold(self) -> None:
        """Handle being asked to go out of bold mode."""
        self.end_markup()

    def reverse(self) -> None:
        """Handle being asked to go to reverse mode."""
        self.begin_markup("ngr")

    def unreverse(self) -> None:
        """Handle being asked to go out of reverse mode."""
        self.end_markup()

    def underline(self) -> None:
        """Handle being asked to go in underline mode."""
        self.begin_markup("ngu")

    def ununderline(self) -> None:
        """Handle being asked to go out of underline mode."""
        self.end_markup()


##############################################################################
def page_title(guide: NortonGuide, entry: Entry | None = None) -> str:
    """Generate a title appropriate for the current page.

    Args:
        guide: The guide that the entry came from.
        entry: The entry to get the title for.

    Returns:
        A title for the current page.
    """

    # Start with the guide title.
    title = [guide.title]

    # If there's a parent menu...
    if entry and entry.parent.has_menu:
        title += [guide.menus[entry.parent.menu].title]

    # If there's a parent menu prompt...
    if entry and entry.parent.has_prompt:
        title += [guide.menus[entry.parent.menu].prompts[entry.parent.prompt]]

    # Join it all up.
    return " » ".join(make_dos_like(part) for part in title)


##############################################################################
def make_loader(templates: Path | None) -> ChoiceLoader:
    """Make the template loader.

    Args:
        templates: Optional directory for template overrides.

    Returns:
        Returns the template loader object.
    """
    loaders: list[FileSystemLoader] = []
    if templates is not None:
        if (templates := templates.expanduser().resolve()).is_dir():
            log(f"Adding {templates} to the template path")
            loaders.append(FileSystemLoader(str(templates), followlinks=True))
        else:
            log(f"Ignoring {templates} as a template location as it does not exist")
    if (local_templates := Path("templates").resolve()).is_dir():
        log(f"Adding {local_templates} to the template path")
        loaders.append(FileSystemLoader(str(local_templates), followlinks=True))
    return ChoiceLoader(loaders + [PackageLoader(Path(__file__).stem)])


##############################################################################
def to_html(args: argparse.Namespace) -> None:
    """Convert a Norton Guide into HTML.

    Args:
        args: The command line arguments.
    """

    # Ensure the guide we're supposed to convert exists.
    if not (convert_from := Path(args.guide).expanduser().resolve()).is_file():
        log(f"No such file: {args.guide}")
        exit(1)

    # Ensure that the directory we're supposed to write to either doesn't
    # exist yet, or does exist and is actually a directory.
    if (
        output_directory := Path(args.output).expanduser().resolve()
    ).exists() and not output_directory.is_dir():
        log(f"Not a directory: {args.output}")
        exit(1)

    # Ensure the output directory exists.
    try:
        output_directory.mkdir(parents=True, exist_ok=True)
    except IOError as error:
        log(f"{error}")
        exit(1)

    with NortonGuide(convert_from) as guide:
        # Log some basics.
        log(f"Guide: {guide.path}")
        log(f"Output directory: {output_directory}")
        log(f"Output prefix: {prefix('', guide)}")

        # Bootstrap the template stuff.
        env = Environment(
            loader=make_loader(args.templates), autoescape=select_autoescape()
        )

        # Set up the global variables for template expansion.
        env.globals = {
            "generator": f"ng2web v{__version__} (ngdb v{ngdb_ver})",
            "guide": guide,
            "about_url": about(guide, output_directory).name,
            "stylesheet": css(guide, output_directory).name,
            "generation_time": datetime.now(),
        }

        # Set up the filters for the guide templates.
        env.filters = {
            "urlify": lambda option: entry_file(
                guide, output_directory, option.offset, args.index
            ).name,
            "toHTML": lambda src: Markup(ToHTML(src)),
            "title": lambda entry: page_title(guide, entry),
        }

        # Write the stylesheet.
        write_css(guide, output_directory, env)

        # Write the about page.
        write_about(guide, output_directory, env)

        # Now, for every entry in the guide...
        for entry in guide:
            write_entry(entry, guide, output_directory, args.index, env)


##############################################################################
# Main entry point for the tool.
def main() -> None:
    """Main entry point for the tool."""
    to_html(get_args())


### ng2web.py ends here
