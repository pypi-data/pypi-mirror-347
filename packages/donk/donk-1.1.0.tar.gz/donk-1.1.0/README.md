# donk

donk is a minimal version management tool for pyproject.toml files.

It does three things:

1. Bump the (`major`|`minor`|`patch`) version in your pyproject.toml file
2. Print the version set in your pyproject.toml file
3. Write the version to a file in your module

## Installation

```shell-session
$ pipx install donk
```

## Usage

```shell-session
$ donk
Usage: donk [OPTIONS] COMMAND [ARGS]...

  donk is a minimal version management tool for pyproject.toml files

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  major  Bump the major version
  minor  Bump the minor version
  patch  Bump the patch version
  show   Display version set in project file

```

## Configuration

You can configure donk to write the version to a python file using the tool
section in pyproject.toml:

```toml
[tool.donk]
write_module_version = "donk/__init__.py"
```

This will write `__version__ = "$current_version"` at the same time as the
version in pyproject.toml is bumped.
