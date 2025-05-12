from pathlib import Path

import click
from charset_normalizer import from_path


def _add_bom(file):
    with open(file, "rb") as f:
        content = f.read()

    with open(file, "wb") as f:
        f.write(b"\xef\xbb\xbf")
        f.write(content)


@click.command()
@click.argument("file")
@click.option("--force", is_flag=True, help="Force add bom to file")
def add_bom(file, force):
    """
    Add a BOM to a file to ensure it opens as UTF-8 in Excel on a Mac.

    FILE is the path to the file to add the BOM to.

    Use --force to add bom to file regardless of detected encoding.
    """
    file = Path(file)

    if not file.exists():
        raise click.ClickException(f"File {file} does not exist")

    encoding = from_path(file).best()
    if encoding.bom:
        raise click.ClickException(
            f"File '{file.name}' already has bom. Cannot continue."
        )

    if force:
        return _add_bom(file)

    if encoding.encoding == "utf_8":
        return _add_bom(file)
    else:
        raise click.ClickException(f"""File '{file.name}' does not look like utf-8.
                                   
Detected encoding: {encoding.encoding}

Use --force to add bom.""")
