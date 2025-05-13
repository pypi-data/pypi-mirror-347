"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """The Python OCSF Library."""


if __name__ == "__main__":
    main(prog_name="py-ocsf")  # pragma: no cover
