"""Resource planning and allocation heuristics for synthetic disaster scenarios."""

from __future__ import annotations

import numpy as np
import pandas as pd


RESOURCE_EFFECTIVENESS = {
    "rescue_team": {"population": 0.90, "flood": 0.80, "wildfire": 0.45},
    "medical_team": {"population": 0.95, "flood": 0.55, "wildfire": 0.55},
    "fire_engine": {"population": 0.45, "flood": 0.20, "wildfire": 0.95},
    "evac_bus": {"population": 0.95, "flood": 0.70, "wildfire": 0.70},
    "water_pump": {"population": 0.30, "flood": 1.00, "wildfire": 0.10},
    "supply_truck": {"population": 0.70, "flood": 0.55, "wildfire": 0.55},
    "drone_team": {"population": 0.35, "flood": 0.65, "wildfire": 0.85},
    "generator": {"population": 0.45, "flood": 0.55, "wildfire": 0.45},
}


def estimate_zone_resource_demand(priority_zones: pd.DataFrame) -> pd.DataFrame:
    """Estimate fictional resource demand by zone from hazard and population context."""
    rows: list[dict] = []
    for zone in priority_zones.itertuples(index=False):
        flood_need = float(zone.flood_intensity) if "flood_intensity" in priority_zones.columns else float(zone.hazard_intensity)
        fire_need = float(zone.wildfire_intensity) if "wildfire_intensity" in priority_zones.columns else float(zone.hazard_intensity)
        population_need = min(float(zone.population) / max(float(priority_zones["population"].max()), 1.0), 1.0)
        rows.append({
            "cell_id": zone.cell_id,
            "x": int(zone.x),
            "y": int(zone.y),
            "rescue_team_need": round(1 + 5 * population_need * zone.hazard_intensity, 2),
            "medical_team_need": round(1 + 4 * population_need * zone.vulnerability_score, 2),
            "fire_engine_need": round(1 + 6 * fire_need, 2),
            "evac_bus_need": round(1 + 5 * population_need * zone.hazard_intensity, 2),
            "water_pump_need": round(1 + 6 * flood_need, 2),
            "supply_truck_need": round(1 + 3 * population_need, 2),
        })
    return pd.DataFrame(rows)


def allocate_resources(priority_zones: pd.DataFrame, resources: pd.DataFrame) -> pd.DataFrame:
    """Assign each resource pool to high-priority zones with transparent scoring.

    This is an auditable planning heuristic, not a dispatch order.
    """
    rows: list[dict] = []
    for resource in resources.itertuples(index=False):
        weights = RESOURCE_EFFECTIVENESS.get(resource.resource_type, {"population": 0.5, "flood": 0.5, "wildfire": 0.5})
        candidates = priority_zones.copy()
        candidates["distance"] = np.sqrt((candidates["x"] - resource.x) ** 2 + (candidates["y"] - resource.y) ** 2)
        candidates["resource_match_score"] = (
            0.35 * candidates["zone_priority_score"]
            + 22 * weights["population"] * np.log1p(candidates["population"]) / np.log1p(max(priority_zones["population"].max(), 1))
            + 18 * weights["flood"] * candidates["flood_intensity"]
            + 18 * weights["wildfire"] * candidates["wildfire_intensity"]
            - 2.2 * candidates["distance"] / max(resource.mobility, 0.05)
        )
        best = candidates.sort_values("resource_match_score", ascending=False).iloc[0]
        deploy_units = int(min(resource.available_units, max(1, round(best["resource_match_score"] / 35))))
        rows.append({
            "resource_id": resource.resource_id,
            "resource_type": resource.resource_type,
            "assigned_cell": best["cell_id"],
            "assigned_x": int(best["x"]),
            "assigned_y": int(best["y"]),
            "available_units": int(resource.available_units),
            "recommended_units": deploy_units,
            "distance_to_zone": round(float(best["distance"]), 2),
            "resource_match_score": round(float(best["resource_match_score"]), 2),
            "planning_note": "planning recommendation only; official dispatch requires human incident command approval",
        })
    return pd.DataFrame(rows).sort_values("resource_match_score", ascending=False).reset_index(drop=True)


def shelter_capacity_summary(exposed_assets: pd.DataFrame, grid: pd.DataFrame) -> dict[str, int | float]:
    """Summarize shelter capacity versus exposed population in the synthetic region."""
    shelters = exposed_assets.loc[exposed_assets["asset_type"] == "shelter"]
    exposed_population = int(grid.loc[grid["hazard_intensity"] >= 0.55, "population"].sum())
    capacity = int(shelters.loc[shelters["exposure_band"].isin(["low", "moderate"]), "capacity"].sum())
    return {
        "exposed_population": exposed_population,
        "usable_shelter_capacity": capacity,
        "estimated_capacity_gap": int(max(exposed_population - capacity, 0)),
        "capacity_coverage_fraction": float(capacity / max(exposed_population, 1)),
    }
