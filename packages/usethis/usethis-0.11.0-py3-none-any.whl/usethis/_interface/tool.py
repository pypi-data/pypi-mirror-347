from typing import Protocol

import typer

from usethis._config import offline_opt, quiet_opt, usethis_config
from usethis._config_file import files_manager
from usethis._console import err_print
from usethis._core.tool import (
    use_codespell,
    use_coverage,
    use_deptry,
    use_import_linter,
    use_pre_commit,
    use_pyproject_fmt,
    use_pyproject_toml,
    use_pytest,
    use_requirements_txt,
    use_ruff,
)
from usethis.errors import UsethisError

app = typer.Typer(
    help="Add and configure development tools, e.g. linters.", add_completion=False
)

how_opt = typer.Option(
    False, "--how", help="Only print how to use the tool, do not add or remove it."
)
remove_opt = typer.Option(
    False, "--remove", help="Remove the tool instead of adding it."
)
frozen_opt = typer.Option(False, "--frozen", help="Use the frozen dependencies.")


@app.command(
    name="codespell",
    help="Use the codespell spellchecker: detect common spelling mistakes.",
    rich_help_panel="Code Quality Tools",
)
def codespell(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_codespell, remove=remove, how=how)


@app.command(
    name="coverage",
    help="Use coverage: a code coverage measurement tool.",
    rich_help_panel="Testing",
)
def coverage(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_coverage, remove=remove, how=how)


@app.command(
    name="deptry",
    help="Use the deptry linter: avoid missing or superfluous dependency declarations.",
    rich_help_panel="Code Quality Tools",
)
def deptry(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_deptry, remove=remove, how=how)


@app.command(
    name="import-linter",
    help="Use Import Linter: enforce a self-imposed architecture on imports.",
    rich_help_panel="Code Quality Tools",
)
def import_linter(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_import_linter, remove=remove, how=how)


@app.command(
    name="pre-commit",
    help="Use the pre-commit framework to manage and maintain pre-commit hooks.",
    rich_help_panel="Code Quality Tools",
)
def pre_commit(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_pre_commit, remove=remove, how=how)


@app.command(
    name="pyproject-fmt",
    help="Use the pyproject-fmt linter: opinionated formatting of 'pyproject.toml' files.",
    rich_help_panel="Code Quality Tools",
)
def pyproject_fmt(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_pyproject_fmt, remove=remove, how=how)


@app.command(
    name="pyproject.toml",
    help="Use a pyproject.toml file to configure the project.",
    rich_help_panel="Configuration Files",
)
def pyproject_toml(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_pyproject_toml, remove=remove, how=how)


@app.command(
    name="pytest", help="Use the pytest testing framework.", rich_help_panel="Testing"
)
def pytest(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_pytest, remove=remove, how=how)


@app.command(
    name="requirements.txt",
    help="Use a requirements.txt file exported from the uv lockfile.",
    rich_help_panel="Configuration Files",
)
def requirements_txt(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_requirements_txt, remove=remove, how=how)


@app.command(
    name="ruff",
    help="Use Ruff: an extremely fast Python linter and code formatter.",
    rich_help_panel="Code Quality Tools",
)
def ruff(
    remove: bool = remove_opt,
    how: bool = how_opt,
    offline: bool = offline_opt,
    quiet: bool = quiet_opt,
    frozen: bool = frozen_opt,
) -> None:
    with (
        usethis_config.set(offline=offline, quiet=quiet, frozen=frozen),
        files_manager(),
    ):
        _run_tool(use_ruff, remove=remove, how=how)


class UseToolFunc(Protocol):
    def __call__(self, *, remove: bool, how: bool) -> None: ...


def _run_tool(caller: UseToolFunc, *, remove: bool, how: bool):
    try:
        caller(remove=remove, how=how)
    except UsethisError as err:
        err_print(err)
        raise typer.Exit(code=1) from None


ALL_TOOL_COMMANDS: list[str] = [
    "codespell",
    "coverage",
    "deptry",
    "import-linter",
    "pre-commit",
    "pyproject.toml",
    "pyproject-fmt",
    "pytest",
    "requirements.txt",
    "ruff",
]
