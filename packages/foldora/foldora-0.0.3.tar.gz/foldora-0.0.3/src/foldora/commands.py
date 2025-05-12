import os
import click
from pathlib import Path
from os.path import isfile, isdir

from foldora.utils import sub_dell, list_path, sub_fill, colorHandler


@click.command(help="List all files and directories of a given path.")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True, file_okay=False, readable=True, path_type=Path),
)
def l(paths):
    """
    List files and directories.

    Lists all files and directories in the current directory or specified paths.

    Arguments:
        paths (tuple of Path): Paths to list. If no paths are provided, lists the contents of the current directory.

    Examples:
        fd list
        fd list /path/to/directory
    """

    if len(paths) < 1:
        click.echo("\t")

        for entry in Path.cwd().iterdir():
            file = colorHandler(f"[FILE] :: {entry.name}", "bright_blue")
            folder = colorHandler(f"[DIR] :: [{entry.name}]", "green")
            click.echo(folder if entry.is_dir() else file, nl=True, color=True)

        click.echo("\t")
        return

    for i, path in enumerate(paths):
        click.echo("\t")

        if len(paths) > 1:
            click.echo(f"({path}):")

        for entry in path.iterdir():
            file = colorHandler(f"[FILE] :: {entry.name}", "bright_blue")
            folder = colorHandler(f"[DIR] :: [{entry.name}]", "green")
            click.echo(folder if entry.is_dir() else file, nl=True, color=True)

        if i > 1:
            click.echo("\t")

    click.echo("\t")


@click.command(help="Create directories and sub-directories.")
@click.argument(
    "path",
    nargs=-1,
    type=click.Path(file_okay=False, exists=False, path_type=Path),
)
def d(path):
    """
    Create directories.

    Creates one or more directories.

    Arguments:
        path (tuple of Path): Paths to directories to be created. If directories already exist, they are not modified.

    Examples:
        fd dirs new_directory another_directory
    """
    if len(path) == 0:
        click.echo(
            colorHandler("\n[!] No path was given.\n", "bright_yellow"),
            color=True,
        )
        return

    for i, p in enumerate(path):
        p.mkdir(parents=True, exist_ok=True)

    click.echo(colorHandler(f"\n[{len(path)}] DIR(s) have been created.\n", "green"))


@click.command(help="Create files in the current (or a given) path.")
@click.option(
    "-p",
    "--path",
    nargs=1,
    type=click.Path(exists=False, path_type=Path),
    help="Custom path where the file(s) will be saved.",
)
@click.argument(
    "paths",
    nargs=-1,
    type=click.File(
        mode="w",
        encoding="utf-8",
    ),
)
def f(paths, path):
    """
    Create files.

    Creates one or more files in the current directory or specified path.

    Arguments:
        paths (tuple of File): Names of files to be created.
        path (Path, optional): Custom path where the files will be created. If not provided, files are created in the current directory.

    Examples:
        fd files file1.txt file2.txt
        fd files file1.txt file2.txt -p /path/to/directory
    """

    if path:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        for f in paths:
            with open(path / f.name, "w") as file:
                file.write("")

        click.echo(colorHandler(f"\n[({len(paths)}] FILE(s) have been created.", "green"))
        return

    if len(paths) == 0:
        click.echo(colorHandler("\n[!] No file path was given.\n", "bright_yellow"))
        return

    for f in paths:
        with open(f.name, "w") as file:
            file.write("")

    click.echo(colorHandler(f"\n[{len(paths)}] FILE(s) have been created.\n", "bright_blue"))


@click.command(help="Purge files and folders.")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, readable=True, path_type=Path),
)
def p(paths):
    """
    Purge files and directories.

    Deletes specified files and directories. Requires user confirmation.

    Arguments:
        paths (tuple of Path): Paths of files and directories to be deleted.

    Examples:
        fd purge file1.txt directory1
    """

    dirs = []
    files = []

    if len(paths) < 1:
        click.echo(colorHandler("\n[!] No path was given.\n", "bright_yellow"))
        return

    click.echo("\t")

    if not click.confirm(text="Proceed with deleting the files/folders ?", abort=True):
        return

    click.echo("\t")

    for i, path in enumerate(paths):

        # Directories
        if path.is_dir():
            sub_dell(path)
            dirs.append(i)

        # Files
        if path.is_file():
            path.unlink(path)
            files.append(i)

    if len(dirs) > 0:
        click.echo(colorHandler(f"[{len(dirs)}] DIR(s) have been removed.", "green"))

    if len(files) > 0:
        click.echo(colorHandler(f"[{len(files)}] FILE(s) have been removed.", "bright_blue"))

    click.echo("\t")


@click.command(help="Show the content of one or more files.")
@click.argument("files", nargs=-1, type=click.File(mode="r"))
def c(files):
    """
    Show file contents.

    Displays the content of one or more files.

    Arguments:
        files (tuple of File): Files to display the contents of.

    Examples:
        fd content file1.txt file2.txt
    """

    if len(files) < 1:
        click.echo(colorHandler("\n[!] No file path was given.\n", "bright_yellow"))
        return

    click.echo("\t")

    for file in files:
        click.echo(colorHandler(f"============[{file.name}]============", "green"), nl=True)
        click.echo("\t")
        click.echo(f"{file.read().strip()}", nl=True)

        if file != files[-1]:
            click.echo("\t")

    click.echo("\t")


@click.command(help="Fills blanks in file and folder names.")
@click.argument(
    "path",
    nargs=1,
    required=False,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, path_type=Path),
)
def b(path: Path):
    """
    Fills blanks in file and folder names by replacing spaces with underscores.

    If the path is not provided, the current directory is used.

    Optionally, the user can activate `Deep Folder Traversal` mode by typing 'y' when prompted,
    which applies a low-level operation to the given path.

    Arguments:
        path (str, optional): Path to the directory or file. If omitted, defaults to the current directory.

    Examples:
        fd b /path/

    Note:
        - Only top-level files and folders are renamed unless `Folder Traversal` is activated.
    """

    sub: str = input("\n[+] Deep Folder Traversal (y/n): ").strip().lower()

    click.echo("\t")

    if not path:
        path = "."

    if sub == "y":
        sub_fill(path)
        click.echo(colorHandler("\n[DONE]\n", "white"), nl=True)
        return

    for df in os.listdir(path):
        origin_path: Path = Path(f"{path}/{df}").resolve()

        if isfile(origin_path):
            os.rename(origin_path, f"{path}/{df.replace(' ', '_')}")

        if isdir(origin_path):
            os.rename(origin_path, f"{path}/{df.replace(' ', '_')}")

    list_path(path)
    click.echo(colorHandler("\n[DONE]\n", "white"), nl=True)
