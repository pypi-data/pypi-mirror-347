# Copyright (C) Izhar Ahmad 2025-2026

from __future__ import annotations

from typing import Any, Iterator
from typing_extensions import Self
from packaging.version import Version, InvalidVersion
from prept.errors import InvalidConfig, ConfigNotFound, BoilerplateNotFound, PreptCLIError
from prept.context import GenerationContext
from prept.variables import TemplateVariable
from prept.cli import outputs
from prept import utils, providers

import re
import os
import json
import click
import pathspec
import pathlib

__all__ = (
    'BoilerplateInfo',
)


PATTERN_BOILERPLATE_NAME = re.compile(r'^[A-Za-z_][A-Za-z0-9_-]*$')
DEFAULT_IGNORED_PATHS = {'preptconfig.json'}


class BoilerplateInfo:
    """Represents a boilerplate.

    This is a wrapper class for information stored in preptconfig.json.
    """
    def __init__(
        self,
        name: str,
        path: pathlib.Path,
        summary: str | None = None,
        version: Version | str | None = None,
        ignore_paths: list[str] | None = None,
        default_generate_directory: str | None = None,
        template_provider: str | None = None,
        template_files: list[str] | None = None,
        template_variables: dict[str, dict[str, Any]] | None = None,
        allow_extra_variables: bool = False,
    ):
        self._path = path
        self.ignore_paths = ignore_paths or []
        self.name = name
        self.summary = summary
        self.version = version
        self.default_generate_directory = default_generate_directory
        self.template_provider = template_provider
        self.template_files = template_files
        self.allow_extra_variables = allow_extra_variables

        if template_variables is None:
            self.template_variables = {}
        else:
            self.template_variables = {
                name: TemplateVariable._from_data(self, name, data)
                for name, data in template_variables.items()
            }

    def _get_generated_files(self) -> Iterator[pathlib.Path]:
        ignore_paths = set(self._ignore_paths).union(DEFAULT_IGNORED_PATHS)
        spec = pathspec.PathSpec.from_lines('gitwildmatch', ignore_paths)

        for file in spec.match_tree(self.path, negate=True):
            yield pathlib.Path(self.path / file).relative_to(self.path)

    def _get_installation_files(self) -> Iterator[pathlib.Path]:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', [])

        for file in spec.match_tree(self.path, negate=True):
            yield pathlib.Path(self.path / file).relative_to(self.path)

    def _get_generation_context(self, output: pathlib.Path, variables: dict[str, Any]) -> GenerationContext:
        return GenerationContext(boilerplate=self, output_dir=output, variables=variables)

    def _is_template_file(self, file: pathlib.Path) -> bool:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', self.template_files)
        return spec.match_file((self.path / file).relative_to(self.path))

    def _resolve_variables(self, input_vars: list[tuple[str, str]]) -> dict[str, Any]:
        resolved = {
            name: value
            for name, value in input_vars
        }
        invalid = set(resolved).difference(self.template_variables)
        if invalid:
            raise PreptCLIError(f'Invalid template variables provided: {", ".join(invalid)}')

        for var_name, var in self.template_variables.items():
            if var_name in resolved:
                continue
            if var.summary:
                click.echo(outputs.cli_msg(f'OPTION', var.summary, prefix_opts={'fg': 'cyan'}))
                prompt = var.name
            else:
                click.echo(outputs.cli_msg(f'OPTION', var.name, prefix_opts={'fg': 'cyan'}))
                prompt = ''
            
            prompt += ' (required)' if var.required else ' (optional)'

            if not var.required and var.default is None:
                # If variable is optional and has no default, set default to
                # UNDEFINED to differentiate from None (Click's representation for no default)
                default = utils.UNDEFINED
            else:
                default = var.default

            click.echo()
            value = click.prompt(
                outputs.cli_msg('', prompt),
                default=default,
                show_default=default is not utils.UNDEFINED,
                value_proc=lambda v: v  # needed to prevent copying of undefined sentinel
            )
            click.echo()

            if value is utils.UNDEFINED:
                continue

            resolved[var_name] = value

        return resolved

    @property
    def path(self) -> pathlib.Path:
        """The :class:`pathlib.Path` pointing towards this boilerplate.

        Note that this is the path where the boilerplate configuration
        file is located, not the generation path.
        """
        return self._path

    @property
    def name(self) -> str:
        """The name of boilerplate.

        Boilerplate names must pass the following set of rules:

        - Consists of alphanumeric, hyphens, and underscores characters.
        - Must begin with a letter or underscore.
        - Names are *not* case-sensitive.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidConfig('name', f'Boilerplate name must be a string; got {name!r} of type {type(name).__qualname__}')
        if not PATTERN_BOILERPLATE_NAME.match(value):
            raise InvalidConfig('name', f'{value!r} is not a valid boilerplate name.')

        self._name = value

    @property
    def summary(self) -> str | None:
        """A summary or brief describing the boilerplate.

        This attribute can be set to ``None`` or ``null`` in preptconfig.json
        which is the default setting.
        """
        return self._summary
    
    @summary.setter
    def summary(self, value: str | None) -> None:
        if value is not None and not isinstance(value, str):
            raise InvalidConfig('summary', f'Boilerplate summary must be a string')

        self._summary = value

    @property
    def version(self) -> Version | None:
        """The version of boilerplate.

        If provided, version must follow the specification described
        in PEP 440: https://peps.python.org/pep-0440/

        This attribute can be set to ``None`` or ``null`` in preptconfig.json
        which is the default setting.
        """
        return self._version
 
    @version.setter
    def version(self, value: Version | str | None) -> None:        
        if value is not None and not isinstance(value, (Version, str)):
            raise InvalidConfig('version', f'{version!r} cannot be parsed as a boilerplate version')

        try:
            self._version = Version(value) if isinstance(value, str) else value
        except InvalidVersion:
            raise InvalidConfig(
                'version',
                f'{value!r} is not a valid boilerplate version',
                'Versions must follow the specification described by PEP 440: https://peps.python.org/pep-0440/'
            )
        
    @property
    def ignore_paths(self) -> list[str]:
        """List of paths that are not included in code generated from boilerplate.

        This option is useful in ignoring any irrelevant paths such as ``.git``. Note
        that Prept automatically ignores boilerplate configuration file regardless of
        the value of this attribute.

        This attribute can be set to ``None`` or ``null`` in preptconfig.json to
        include every file and directory which is the default setting.
        """
        return self._ignore_paths

    @ignore_paths.setter
    def ignore_paths(self, value: list[str] | None) -> None:
        if value is None:
            value = []
        if list(filter(lambda v: not isinstance(v, str), value)):
            raise InvalidConfig('ignore_paths', 'ignore_paths cannot contain non-string entries')

        self._ignore_paths = value

    @property
    def default_generate_directory(self) -> str:
        """The default directory that boilerplate generates code in.

        This directory is used (or created) if user does not specify
        `-O` in "prept new" command.

        If not provided or is None, defaults to the name of boilerplate at
        the time of generation.
        """
        return self._default_generate_directory or self._name

    @default_generate_directory.setter
    def default_generate_directory(self, value: str | None) -> None:
        if value is not None and not isinstance(value, str):
            raise InvalidConfig('default_generate_directory', 'default_generate_directory must be a string')

        self._default_generate_directory = value

    @property
    def template_provider(self) -> type[providers.TemplateProvider] | None:
        """The name of template provider for this boilerplate, if any.
        
        Template providers act as middleware for processing template
        files. See documentation of :class:`TemplateProvider` for
        more information.

        By default, no template provider is set. Prept provides two built-in
        template providers by default:

        - ``string-sub`` for $-substitutions
        - ``jinja2`` based on Jinja templates (requires Jinja2 installed)

        This option can take name of third party template providers as well
        using ``::`` to separate package name and template provider name. For
        example, ``foobar::baz`` means ``baz`` template provider from the ``foobar``
        package or module.
        """
        return self._template_provider
    
    @template_provider.setter
    def template_provider(self, value: type[providers.TemplateProvider] | str | None) -> None:
        if value is None:
            self._template_provider = None
            return
        if isinstance(value, str):
            value = providers.resolve_template_provider(value)

        # See comment in TemplateProvider for explanation of why getattr()
        # is used here instead of issubclass() with TemplateProvider
        if not getattr(value, '__prept_template_provider__', False):
            raise InvalidConfig('template_provider', 'Invalid template provider, not a subclass of TemplateProvider')

        self._template_provider = value

    @property
    def template_files(self) -> list[str]:
        """List of file paths (as patterns) that are templates.

        These files are processed by the given template provider which
        must also be set for this option to have any effect.

        Note that this is a list of gitignore like patterns similar to
        :attr:`.ignore_paths` setting so it is possible to include/exclude
        all files at a specific path.
        """
        return self._template_files

    @template_files.setter
    def template_files(self, value: list[str] | None) -> None:
        if value is None:
            value = []
        if list(filter(lambda v: not isinstance(v, str), value)):
            raise InvalidConfig('template_files', 'template_files cannot contain non-string entries')

        self._template_files = value

    @property
    def allow_extra_variables(self) -> bool:
        """Whether arbitrary variables that are not in template_variables are allowed.

        This is false by default. If set to true, arbitrary variables are allowed
        through the ``-V`` option in ``prept new`` command.
        """
        return self._allow_extra_variables
    
    @allow_extra_variables.setter
    def allow_extra_variables(self, value: bool | None) -> None:
        if value is None:
            value = False
        if not isinstance(value, bool):
            raise InvalidConfig('allow_extra_variables', 'allow_extra_variables must be a boolean value')
        
        self._allow_extra_variables = value

    @classmethod
    def from_path(cls, path: pathlib.Path | str) -> Self:
        """Loads boilerplate information from its path.

        Raises :class:`ConfigNotFound` or :class:`InvalidConfig` if boilerplate
        configuration does not exist or is invalid, respectively.

        Parameters
        ~~~~~~~~~~
        path: :class:`pathlib.Path` | :class:`str`
            The path to boilerplate directory.

        Returns
        ~~~~~~~
        :class:`BoilerplateInfo`
            The loaded boilerplate.
        """
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)

        try:
            with open(path / 'preptconfig.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            if isinstance(e, FileNotFoundError):
                raise ConfigNotFound
            else:
                raise InvalidConfig(None)

        if 'name' not in data:
            raise InvalidConfig(key='name', missing=True)

        return cls(
            name=data['name'],
            path=path,
            summary=data.get('summary'),
            version=data.get('version'),
            ignore_paths=data.get('ignore_paths'),
            default_generate_directory=data.get('default_generate_directory'),
            template_provider=data.get('template_provider'),
            template_files=data.get('template_files'),
            template_variables=data.get('template_variables'),
            allow_extra_variables=data.get('allow_extra_variables'),
        )
    
    @classmethod
    def from_installation(cls, name: str) -> Self:
        """Loads boilerplate from the installation.

        Raises :class:`ConfigNotFound` or :class:`InvalidConfig` if boilerplate
        configuration does not exist or is invalid, respectively. If boilerplate
        does not exist, then :class:`BoilerplateNotFound` is raised.

        Parameters
        ~~~~~~~~~~
        name: :class:`str`
            The name of boilerplate.

        Returns
        ~~~~~~~
        :class:`BoilerplateInfo`
            The loaded boilerplate.
        """
        bp_dir = utils.get_prept_dir('boilerplates', name.lower())

        if not bp_dir.exists():
            raise BoilerplateNotFound(name)
        
        return cls.from_path(bp_dir)

    @classmethod
    def resolve(cls, value: Any) -> Self:
        """Resolves a boilerplate from given value.

        The resolution order is as follows:

        - The passed value is first tested as path and if the path exists, boilerplate
          is loaded from this path if possible.

        - If path resolution fails, boilerplate is loaded from installation.

        
        If boilerplate cannot be resolved through any step, the :class:`BoilerplateNotFound`
        error is raised.

        Returns
        ~~~~~~~
        :class:`BoilerplateInfo`
            The loaded boilerplate.
        """
        if isinstance(value, (pathlib.Path, str)) and os.path.exists(value):
            try:
                return cls.from_path(value)
            except Exception as e:
                if not isinstance(e, ConfigNotFound):
                    # If from_path() fails (i.e. no preptconfig.json in given path), we
                    # silently ignore it and continue to next way of resolution. For any
                    # other error, raise it.
                    raise

        return cls.from_installation(str(value))

    def dump(self) -> dict[str, Any]:
        """Returns the boilerplate in raw data form.

        The result is compatible with the preptconfig.json schema.
        """
        data: dict[str, Any] = {
            "name": self._name,
        }

        if self._summary:
            data['summary'] = self._summary

        if self._version:
            data['version'] = self._version
        
        if self._ignore_paths:
            data['ignore_paths'] = self._ignore_paths

        if self._default_generate_directory:
            data['default_generate_directory'] = self._default_generate_directory

        if self._template_provider:
            data['template_provider'] = self._template_provider

        if self._template_files:
            data['ignore_paths'] = self._ignore_paths

        if self.template_variables:
            data['template_variables'] = {v.name: v._dump() for v in self.template_variables.values()}

        if self._allow_extra_variables:
            data['allow_extra_variables'] = self.allow_extra_variables

        return data

    def save(self) -> None:
        """Saves the boilerplate configuration.

        If configuration is not already present (boilerplate is not initialized), it
        is saved hence initializing the boilerplate.
        """
        with open(self.path, 'w') as f:
            json.dump(self.dump(), f, indent=4)
