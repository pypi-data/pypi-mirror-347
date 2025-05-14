# pyright: standard

"""btrfs-backup-ng: btrfs_backup_ng/endpoint/__init__.py."""

import urllib.parse
from pathlib import Path

from .local import LocalEndpoint
from .shell import ShellEndpoint
from .ssh import SSHEndpoint


def choose_endpoint(spec, common_kwargs=None, source=False, excluded_types=()):
    """Chooses a suitable endpoint based on the specification given.
    If ``common_kwargs`` is given, it should be a dictionary with
    keyword arguments that all endpoint types should be initialized
    with.
    If ``source`` is set, this is considered as a source endpoint,
    meaning that parsed path is passed as ``source`` parameter and not
    as ``path`` at endpoint initialization. The value for ``path``
    should be present in ``common_kwargs`` in this case.
    The endpoint classes specified in ``excluded_types`` are excluded
    from the consideration.
    It will return an instance of the proper ``Endpoint`` subclass.
    If no endpoint can be determined for the given specification,
    a ``ValueError`` is raised.
    """
    kwargs = {}
    if common_kwargs:
        kwargs.update(common_kwargs)

    # parse destination string
    if ShellEndpoint not in excluded_types and spec.startswith("shell://"):
        c = ShellEndpoint
        kwargs["cmd"] = spec[8:]
        kwargs["source"] = True
    elif SSHEndpoint not in excluded_types and spec.startswith("ssh://"):
        c = SSHEndpoint
        parsed = urllib.parse.urlparse(spec)
        if not parsed.hostname:
            msg = "No hostname for SSH specified."
            raise ValueError(msg)
        try:
            kwargs["port"] = parsed.port
        except ValueError:
            # invalid literal for int ...
            kwargs["port"] = None
        path = Path(parsed.path.strip() or "/")
        # This is no URL, so an eventual query part must be appended to path
        if parsed.query:
            path /= "?" + parsed.query
        if source:
            kwargs["source"] = path
        else:
            kwargs["path"] = path
        kwargs["username"] = parsed.username
        kwargs["hostname"] = parsed.hostname
    elif LocalEndpoint not in excluded_types:
        c = LocalEndpoint
        if source:
            kwargs["source"] = Path(spec)
        else:
            kwargs["path"] = Path(spec)
    else:
        msg = f"No endpoint could be generated for this specification: {spec}"
        raise ValueError(
            msg,
        )

    return c(**kwargs)
