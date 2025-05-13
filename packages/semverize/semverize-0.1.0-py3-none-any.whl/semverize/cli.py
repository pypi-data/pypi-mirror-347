import click


@click.command()
@click.argument("PEP_440_VERSION")
def semverize(pep_440_version: str) -> None:
    """Coerce PEP 440 to SemVer, when possible."""
    from . import pep440_to_semver
    import sys

    try:
        semver = pep440_to_semver(pep_440_version)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    print(semver, end="")


if __name__ == "__main__":  # pragma: no cover
    semverize()
