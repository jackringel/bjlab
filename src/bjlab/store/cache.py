"""Key-value stores with a get-or-compute primitive.

Keys are arbitrary strings; values must be JSON-serializable and must not be
``None`` (``None`` is the "miss" sentinel).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable


class Store:
    """Abstract fetch-or-compute cache."""

    def get(self, key: str) -> Any | None:
        """Stored value, or None on a miss."""
        raise NotImplementedError

    def put(self, key: str, value: Any) -> None:
        raise NotImplementedError

    def get_or_compute(self, key: str, compute: Callable[[], Any]) -> Any:
        """The fetch-or-compute pattern every layer uses: return the cached
        value if present, else compute, store, and return it."""
        cached = self.get(key)
        if cached is not None:
            return cached
        value = compute()
        self.put(key, value)
        return value


class InMemoryStore(Store):
    """Dict-backed store for tests and throwaway runs."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def get(self, key: str) -> Any | None:
        return self._data.get(key)

    def put(self, key: str, value: Any) -> None:
        if value is None:
            raise ValueError("None cannot be stored (it is the miss sentinel)")
        self._data[key] = value


class JsonStore(Store):
    """One JSON file per key under ``root`` (default ``~/.bjlab/cache``).

    Filenames are the sha256 of the key, so keys may contain characters that
    are illegal in filenames (``:`` on Windows, ``/`` everywhere). The key
    is stored inside the payload and checked on read.
    """

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root is not None else Path.home() / ".bjlab" / "cache"
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return self.root / f"{digest}.json"

    def get(self, key: str) -> Any | None:
        path = self._path(key)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("key") != key:
            return None
        return payload["value"]

    def put(self, key: str, value: Any) -> None:
        if value is None:
            raise ValueError("None cannot be stored (it is the miss sentinel)")
        payload = json.dumps({"key": key, "value": value})
        self._path(key).write_text(payload, encoding="utf-8")
