from __future__ import annotations

import sys
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer
from typer import Argument, Option

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

app = typer.Typer(add_completion=False)


class OutputFormat(StrEnum):
    typ = "typ"
    pdf = "pdf"
    auto = "auto"


@app.command(name="typsync")
def cli(
    files: Annotated[
        list[Path] | None,
        Argument(
            help="Typst files or directories to process.",
            show_default=False,
        ),
    ] = None,
    *,
    output_format: Annotated[
        OutputFormat,
        Option(
            "--to",
            "-t",
            help="Specify output format (typ or pdf).",
            show_default="auto",
        ),
    ] = OutputFormat.auto,
    output: Annotated[
        Path | None,
        Option(
            "--output",
            "-o",
            metavar="FILE",
            help="Write output to FILE. Use .typ or .pdf extension to control format.",
            show_default=False,
        ),
    ] = None,
    notebook_dir: Annotated[
        Path | None,
        Option(
            "--notebook-dir",
            "-n",
            metavar="DIRECTORY",
            help="Path to Jupyter notebooks containing figures to embed.",
            show_default=False,
        ),
    ] = None,
    citeproc: Annotated[
        bool,
        Option(
            "--citeproc",
            "-C",
            help="Process citations using Zotero integration.",
        ),
    ] = False,
    version: Annotated[
        bool,
        Option(
            "--version",
            "-v",
            help="Display version information and exit.",
        ),
    ] = False,
) -> None:
    """Convert Typst to PDF."""
    if version:
        show_version()

    from nbstore import Store

    text = get_text(files)

    if output_format == OutputFormat.auto:
        output_format = get_output_format(output)

    if output_format == OutputFormat.pdf and not output:
        typer.secho("No output file. Aborted.", fg="red")
        raise typer.Exit(1)

    if notebook_dir:
        store = Store(notebook_dir.absolute())
        typer.echo(store)

    typer.echo(citeproc)

    result = text

    if not output and isinstance(result, str):
        typer.echo(result)


def get_text(files: list[Path] | None) -> str:
    if files:
        it = (file.read_text(encoding="utf8") for file in collect(files))
        return "\n\n".join(it)

    if text := sys.stdin.read():
        return text

    typer.secho("No input text. Aborted.", fg="red")
    raise typer.Exit(1)


def collect(files: Iterable[Path]) -> Iterator[Path]:
    for file in files:
        if file.is_dir():
            for dirpath, dirnames, filenames in file.walk():
                dirnames.sort()
                for filename in sorted(filenames):
                    if filename.endswith(".typ"):
                        yield dirpath / filename

        elif file.suffix == ".typ":
            yield file


def get_output_format(output: Path | None) -> OutputFormat:
    if not output or output.suffix == ".typ":
        return OutputFormat.typ

    if output.suffix == ".pdf":
        return OutputFormat.pdf

    typer.secho(f"Unknown output format: {output.suffix}", fg="red")
    raise typer.Exit(1)


def show_version() -> None:
    from importlib.metadata import version

    typer.echo(f"typsync {version('typsync')}")
    raise typer.Exit
