"""Emergency alert prioritization for synthetic disaster intelligence scenarios."""

from __future__ import annotations

import numpy as np
import pandas as pd


ASSET_IMPORTANCE = {"hospital": 1.0, "fire_station": 0.95, "power_station": 0.95, "shelter": 0.85, "bridge": 0.75, "water_pump": 0.72, "school": 0.55}


def generate_zone_alerts(priority_zones: pd.DataFrame, exposed_assets: pd.DataFrame, confidence: float = 0.82) -> pd.DataFrame:
    """Create transparent, ranked alerts from priority zones and asset exposure."""
    rows: list[dict] = []
    for index, zone in enumerate(priority_zones.itertuples(index=False)):
        local_assets = exposed_assets.loc[exposed_assets["cell_id"] == zone.cell_id]
        max_asset = float(local_assets["asset_exposure_score"].max()) if not local_assets.empty else 0.0
        highest_asset_type = str(local_assets.iloc[0]["asset_type"]) if not local_assets.empty else "none"
        asset_factor = ASSET_IMPORTANCE.get(highest_asset_type, 0.35)
        score = 100 * (0.34 * zone.hazard_intensity + 0.26 * zone.vulnerability_score + 0.18 * min(zone.population / max(priority_zones["population"].max(), 1), 1) + 0.14 * asset_factor + 0.08 * confidence)
        severity = "critical" if score >= 82 else "high" if score >= 64 else "moderate" if score >= 45 else "watch"
        rows.append({
            "alert_id": f"ALERT-{index + 1:03d}",
            "cell_id": zone.cell_id,
            "x": int(zone.x),
            "y": int(zone.y),
            "severity": severity,
            "priority_score": round(float(score), 2),
            "confidence": confidence,
            "hazard_intensity": round(float(zone.hazard_intensity), 3),
            "population": int(zone.population),
            "vulnerability_score": round(float(zone.vulnerability_score), 3),
            "top_asset_type": highest_asset_type,
            "max_asset_exposure_score": round(max_asset, 2),
            "recommended_focus": _recommended_focus(zone.hazard_intensity, highest_asset_type, zone.population),
        })
    return pd.DataFrame(rows).sort_values("priority_score", ascending=False).reset_index(drop=True)


def _recommended_focus(hazard: float, asset_type: str, population: int) -> str:
    if asset_type in {"hospital", "fire_station", "power_station"}:
        return "protect critical infrastructure and verify continuity of service"
    if population >= 100:
        return "prioritize population warning, sheltering, and evacuation assistance"
    if hazard >= 0.75:
        return "monitor rapid hazard escalation and road access"
    return "maintain situational awareness and prepare reserve resources"
