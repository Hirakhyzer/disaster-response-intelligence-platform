"""Configuration, reproducibility, and local-output helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import random

import numpy as np
import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file."""
    with Path(path).open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ValueError(f"Configuration {path} must be a YAML mapping.")
    return config


def set_seed(seed: int) -> None:
    """Seed Python and NumPy for deterministic synthetic scenarios."""
    random.seed(seed)
    np.random.seed(seed)


def ensure_output_dirs(base: str | Path = "outputs") -> dict[str, Path]:
    """Create local output folders excluded from version control."""
    root = Path(base)
    folders = {
        "root": root,
        "figures": root / "figures",
        "results": root / "results",
        "reports": root / "reports",
        "maps": root / "maps",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    return folders
