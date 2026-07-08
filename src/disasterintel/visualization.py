"""Maps and figures generated from local synthetic or authorized disaster runs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _path(path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination


def plot_hazard_map(grid: pd.DataFrame, assets: pd.DataFrame, path: str | Path) -> None:
    """Plot synthetic hazard intensity with infrastructure overlays."""
    pivot = grid.pivot(index="y", columns="x", values="hazard_intensity")
    figure, axis = plt.subplots(figsize=(8.4, 7.2))
    image = axis.imshow(pivot.values, origin="lower", aspect="equal")
    figure.colorbar(image, ax=axis, label="Hazard intensity")
    for asset_type, group in assets.groupby("asset_type"):
        axis.scatter(group["x"], group["y"], s=34, label=asset_type, edgecolor="black", linewidth=0.25)
    axis.set(xlabel="Synthetic x-coordinate", ylabel="Synthetic y-coordinate", title="Synthetic hazard intensity and infrastructure exposure")
    axis.legend(loc="upper right", fontsize=7, ncol=2)
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)


def plot_vulnerability_map(grid: pd.DataFrame, priority_zones: pd.DataFrame, path: str | Path) -> None:
    """Plot vulnerability score with priority-zone markers."""
    pivot = grid.pivot(index="y", columns="x", values="vulnerability_score")
    figure, axis = plt.subplots(figsize=(8.4, 7.2))
    image = axis.imshow(pivot.values, origin="lower", aspect="equal")
    figure.colorbar(image, ax=axis, label="Vulnerability score")
    axis.scatter(priority_zones["x"], priority_zones["y"], marker="x", s=75, label="Priority zones")
    axis.set(xlabel="Synthetic x-coordinate", ylabel="Synthetic y-coordinate", title="Synthetic population vulnerability and priority zones")
    axis.legend(loc="upper right")
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)


def plot_resource_allocations(grid: pd.DataFrame, resources: pd.DataFrame, assignments: pd.DataFrame, path: str | Path) -> None:
    """Plot resource home positions and assigned zones."""
    figure, axis = plt.subplots(figsize=(8.4, 7.2))
    axis.scatter(grid["x"], grid["y"], c=grid["hazard_intensity"], s=10, alpha=0.45)
    for row in assignments.merge(resources[["resource_id", "x", "y"]], on="resource_id", suffixes=("_assigned", "_home")).itertuples(index=False):
        axis.plot([row.x, row.assigned_x], [row.y, row.assigned_y], linewidth=1.2, alpha=0.75)
        axis.scatter(row.x, row.y, marker="s", s=55)
        axis.scatter(row.assigned_x, row.assigned_y, marker="*", s=90)
    axis.set(xlabel="Synthetic x-coordinate", ylabel="Synthetic y-coordinate", title="Resource allocation plan: bases to priority zones")
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)


def plot_alert_priority(alerts: pd.DataFrame, path: str | Path) -> None:
    """Plot alert priority by ranked zone."""
    ordered = alerts.sort_values("priority_score", ascending=True)
    labels = ordered["alert_id"] + "\n" + ordered["cell_id"]
    figure, axis = plt.subplots(figsize=(8.5, 5.2))
    axis.barh(labels, ordered["priority_score"])
    axis.set(xlabel="Priority score", ylabel="Alert / zone", title="Ranked disaster-response alerts")
    axis.grid(True, axis="x", alpha=0.25)
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)


def plot_weather_series(weather: pd.DataFrame, path: str | Path) -> None:
    """Plot synthetic hazard-driving weather indices over time."""
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(weather["timestamp"], weather["rainfall_index"], label="Rainfall index")
    axis.plot(weather["timestamp"], weather["wind_index"], label="Wind index")
    axis.plot(weather["timestamp"], weather["temperature_index"], label="Temperature index")
    axis.set(xlabel="Time", ylabel="Index value", title="Synthetic hazard-driving weather time series")
    axis.grid(True, alpha=0.25); axis.legend()
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)
