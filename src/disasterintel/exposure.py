"""Exposure and infrastructure vulnerability scoring."""

from __future__ import annotations

import numpy as np
import pandas as pd


CRITICALITY_WEIGHT = {"low": 0.25, "medium": 0.50, "high": 0.75, "critical": 1.00}


def score_asset_exposure(grid: pd.DataFrame, assets: pd.DataFrame) -> pd.DataFrame:
    """Attach hazard, population, and vulnerability context to infrastructure assets."""
    context = grid[["cell_id", "hazard_intensity", "flood_intensity", "wildfire_intensity", "population", "vulnerability_score", "drainage", "elevation"]]
    output = assets.merge(context, on="cell_id", how="left", validate="many_to_one")
    if output["hazard_intensity"].isna().any():
        raise ValueError("Some assets did not join to a hazard cell.")
    criticality = output["criticality"].map(CRITICALITY_WEIGHT).fillna(0.5)
    output["asset_exposure_score"] = np.clip(
        100 * (0.40 * output["hazard_intensity"] + 0.30 * output["vulnerability_score"] + 0.30 * criticality), 0, 100
    ).round(2)
    output["exposure_band"] = pd.cut(output["asset_exposure_score"], bins=[-1, 35, 60, 80, 101], labels=["low", "moderate", "high", "severe"]).astype(str)
    return output.sort_values("asset_exposure_score", ascending=False).reset_index(drop=True)


def summarize_population_exposure(grid: pd.DataFrame) -> dict[str, float | int]:
    """Summarize fictional population exposure for briefing and regression tests."""
    exposed = grid.loc[grid["hazard_intensity"] >= 0.55]
    severe = grid.loc[grid["hazard_intensity"] >= 0.75]
    vulnerable_people = (exposed["population"] * exposed["vulnerable_fraction"]).sum()
    return {
        "total_population": int(grid["population"].sum()),
        "exposed_population": int(exposed["population"].sum()),
        "severe_hazard_population": int(severe["population"].sum()),
        "estimated_vulnerable_exposed_population": int(round(vulnerable_people)),
        "mean_hazard_intensity": float(grid["hazard_intensity"].mean()),
        "max_hazard_intensity": float(grid["hazard_intensity"].max()),
    }


def identify_priority_zones(grid: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
    """Return top grid cells by vulnerability and population exposure."""
    zones = grid.copy()
    zones["zone_priority_score"] = (100 * (0.45 * zones["hazard_intensity"] + 0.35 * zones["vulnerability_score"] + 0.20 * np.log1p(zones["population"]) / np.log1p(max(zones["population"].max(), 1)))).round(2)
    return zones.sort_values("zone_priority_score", ascending=False).head(top_n).reset_index(drop=True)
