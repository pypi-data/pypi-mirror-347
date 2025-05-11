import typing as t

import click
import semver
import tomlkit


class TomlFilePath(click.Path):
    name = "tomlfilepath"

    def __init__(
        self,
        exists: bool = True,
        file_okay: bool = True,
        dir_okay: bool = False,
        writable: bool = True,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: t.Optional[t.Type[t.Any]] = None,
        executable: bool = False,
    ):
        super().__init__(
            exists,
            file_okay,
            dir_okay,
            writable,
            readable,
            resolve_path,
            allow_dash,
            path_type,
            executable,
        )
        self.content = None
        self.filepath = None
        self.version = None

    def convert(self, value, param, ctx):
        filepath = super().convert(value, param, ctx)
        self.filepath = filepath
        with open(filepath, "r") as fp:
            try:
                self.content = tomlkit.load(fp)
            except Exception as e:
                self.fail(f"Failed to parse TOML file: {e}", param, ctx)
            finally:
                fp.close()
        self.config = self.content.get("tool", {}).get("donk", {})
        return self

    def __setitem__(self, key: str, value: t.Any):
        self.content[key] = value

    def __getitem__(self, key: str):
        return self.content[key]

    def _get_version(self, section, key) -> semver.Version:
        return semver.Version.parse(self.content[section][key])

    def _set_version(self, section, key, version):
        self.content[section][key] = str(version)
        self.version = version

    def bump_major(self, section: str, key: str):
        version = self._get_version(section, key)
        version = version.bump_major()
        self._set_version(section, key, version)

    def bump_minor(self, section: str, key: str):
        version = self._get_version(section, key)
        version = version.bump_minor()
        self._set_version(section, key, version)

    def bump_patch(self, section: str, key: str):
        version = self._get_version(section, key)
        version = version.bump_patch()
        self._set_version(section, key, version)

    def write(self):
        with open(self.filepath, "w") as fp:
            tomlkit.dump(self.content, fp)

        write_module_version = self.config.get("write_module_version")
        if write_module_version:
            with open(write_module_version, "w") as fp:
                fp.write(f'__version__ = "{self.version}"\n')
