import sys

import click

from . import __version__
from .param_types import TomlFilePath


class ReturnCode(object):
    OK = 0
    UNKNOWN_ERROR = 1


@click.group()
@click.version_option(
    message=f"donk {__version__}", version=__version__, prog_name="donk"
)
def cli():
    """donk is version management tool for pyproject.toml files"""


@cli.command("show")
@click.argument(
    "tomlfile",
    type=TomlFilePath(),
    default="pyproject.toml",
)
@click.option(
    "-s", "--section", help="toml section containg the version key", default="project"
)
@click.option(
    "-k", "--key", help="key in toml section that contains version", default="version"
)
def show(tomlfile, section="project", key="version"):
    """Display version set in project file"""
    click.echo(tomlfile[section][key])


@cli.command("major")
@click.argument(
    "tomlfile",
    type=TomlFilePath(),
    default="pyproject.toml",
)
@click.option(
    "-s", "--section", help="toml section containg the version key", default="project"
)
@click.option(
    "-k", "--key", help="key in toml section that contains version", default="version"
)
def major(tomlfile, section="project", key="version"):
    """Bump the major version"""
    tomlfile.bump_major(section, key)
    tomlfile.write()


@cli.command("minor")
@click.argument(
    "tomlfile",
    type=TomlFilePath(),
    default="pyproject.toml",
)
@click.option(
    "-s", "--section", help="toml section containg the version key", default="project"
)
@click.option(
    "-k", "--key", help="key in toml section that contains version", default="version"
)
def minor(tomlfile, section="project", key="version"):
    """Bump the minor version"""
    tomlfile.bump_minor(section, key)
    tomlfile.write()


@cli.command("patch")
@click.argument(
    "tomlfile",
    type=TomlFilePath(),
    default="pyproject.toml",
)
@click.option(
    "-s", "--section", help="toml section containg the version key", default="project"
)
@click.option(
    "-k", "--key", help="key in toml section that contains version", default="version"
)
def patch(tomlfile, section="project", key="version"):
    """Bump the patch version"""
    tomlfile.bump_patch(section, key)
    tomlfile.write()


def run(as_module: bool = False):
    try:
        return_code = cli.main(
            args=sys.argv[1:],
            prog_name="python -m donk" if as_module else "donk",
            standalone_mode=False,
        )
    except Exception as e:
        click.secho(str(e), fg="red", err=True)
        return_code = ReturnCode.UNKNOWN_ERROR
    sys.exit(return_code)
