"""Optional polars DataFrame conversion utility."""

from __future__ import annotations

from typing import Any


def to_dataframe(data: list[dict[str, Any]] | dict[str, Any]) -> Any:
    """Convert a list of dicts (or a dict with a data key) to a polars DataFrame.

    Requires: pip install nseindiapy[polars]

    Args:
        data: List of dicts, or a dict containing a list under a known key.

    Returns:
        polars.DataFrame
    """
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "polars is required for as_df=True. Install with: pip install nseindiapy[polars]"
        )

    if isinstance(data, dict):
        # Try common NSE response shapes
        for key in ("data", "records", "results"):
            if key in data and isinstance(data[key], list):
                return pl.DataFrame(data[key])
        # If it's a single-record dict, wrap it
        return pl.DataFrame([data])

    return pl.DataFrame(data)
