"""Resolve TAMPINHA_HOME for standalone skill scripts.

Skill scripts may run outside the Tampinha process (e.g. system Python,
nix env, CI) where ``tampinha_constants`` is not importable.  This module
provides the same ``get_tampinha_home()`` and ``display_tampinha_home()``
contracts as ``tampinha_constants`` without requiring it on ``sys.path``.

When ``tampinha_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``tampinha_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``TAMPINHA_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from tampinha_constants import display_tampinha_home as display_tampinha_home
    from tampinha_constants import get_tampinha_home as get_tampinha_home
except (ModuleNotFoundError, ImportError):

    def get_tampinha_home() -> Path:
        """Return the Tampinha home directory (default: ~/.tampinha).

        Mirrors ``tampinha_constants.get_tampinha_home()``."""
        val = os.environ.get("TAMPINHA_HOME", "").strip()
        return Path(val) if val else Path.home() / ".tampinha"

    def display_tampinha_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``tampinha_constants.display_tampinha_home()``."""
        home = get_tampinha_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
