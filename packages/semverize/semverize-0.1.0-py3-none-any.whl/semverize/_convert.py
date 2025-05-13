def pep440_to_semver(pep440_version: str) -> str:
    """
    Convert a PEP 440 version to a SemVer version. Throws ValueError if the PEP
    440 version can't be converted to SemVer.

    Args:
        pep440_version (str): The PEP 440 version string.

    Returns:
        str: The SemVer version string.
    """
    from semver import Version as SemverVersion
    from packaging.version import Version as Pep440Version

    in_version = Pep440Version(pep440_version)

    if in_version.epoch != 0:
        raise ValueError(
            "Can't convert a PEP 440 version with a non-zero epoch to SemVer"
        )
    if in_version.post is not None:
        raise ValueError(
            "Can't convert a PEP 440 version with a post component to SemVer"
        )
    if in_version.local is not None:
        raise ValueError(
            "Can't convert a PEP 440 version with a local component to SemVer"
        )

    if in_version.pre is None:
        pre = None
    else:
        if in_version.pre[0] == "a":
            pre = "alpha"
        elif in_version.pre[0] == "b":
            pre = "beta"
        elif in_version.pre[0] == "rc":
            pre = "rc"
        else:  # pragma: no cover
            raise ValueError(
                f"Can't convert PEP 440 version with unknown pre-release component {in_version.pre[0]} to SemVer"
            )
        pre += f".{in_version.pre[1]}"

    if in_version.dev is None:
        dev = None
    else:
        dev = f"dev.{in_version.dev}"

    return str(
        SemverVersion(
            major=in_version.major,
            minor=in_version.minor,
            patch=in_version.micro,
            prerelease=pre,
            build=dev,
        )
    )
