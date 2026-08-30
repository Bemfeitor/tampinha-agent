"""Resolve TAMPINHA_HOME for standalone skill scripts.

Skill scripts may run outside the Tampinha process (system Python, nix env,
CI) where ``tampinha_constants`` is not importable.  This module provides the
same ``get_tampinha_home()`` contract without requiring it on ``sys.path``.

When ``tampinha_constants`` IS available it is used directly so profile
resolution and any future enhancements are picked up automatically.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from tampinha_constants import get_tampinha_home as get_tampinha_home
except (ModuleNotFoundError, ImportError):

    def get_tampinha_home() -> Path:
        """Return the Tampinha home directory (default: ``~/.tampinha``)."""
        val = os.environ.get("TAMPINHA_HOME", "").strip()
        return Path(val) if val else Path.home() / ".tampinha"
