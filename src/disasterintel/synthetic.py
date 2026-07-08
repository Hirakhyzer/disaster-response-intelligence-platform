"""Deterministic synthetic climate and disaster scenario generator.

The generator creates a fictional region with hazard intensity layers, population
vulnerability, infrastructure assets, response resources, and road links. It is
for safe research demonstrations only and is not an official warning, map, or
emergency-management dataset.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticDisasterConfig:
    """Controls reproducible synthetic region generation."""

    grid_size: int = 32
    seed: int = 42
    scenario: str = "combined"  # flood, wildfire, or combined

    def __post_init__(self) -> None:
        if self.grid_size < 12:
            raise ValueError("grid_size must be at least 12 for meaningful maps and routes.")
        if self.scenario not in {"flood", "wildfire", "combined"}:
            raise ValueError("scenario must be flood, wildfire, or combined.")


def generate_synthetic_region(config: SyntheticDisasterConfig | None = None) -> dict[str, pd.DataFrame]:
    """Return synthetic grid, assets, resources, road links, and time-series weather."""
    cfg = config or SyntheticDisasterConfig()
    rng = np.random.default_rng(cfg.seed)
    grid = _grid(cfg, rng)
    assets = _infrastructure_assets(grid, rng)
    resources = _response_resources(grid, rng)
    roads = _road_links(cfg.grid_size, grid, rng)
    weather = _weather_series(cfg, rng)
    return {"grid": grid, "assets": assets, "resources": resources, "roads": roads, "weather": weather}


def _grid(cfg: SyntheticDisasterConfig, rng: np.random.Generator) -> pd.DataFrame:
    size = cfg.grid_size
    x, y = np.meshgrid(np.arange(size), np.arange(size))
    x = x.ravel(); y = y.ravel()
    center_x, center_y = size * 0.45, size * 0.56
    river_distance = np.abs(y - (0.55 * size + 2.2 * np.sin(x / 4.7)))
    elevation = 55 + 1.8 * y + 0.7 * x + rng.normal(0, 3.0, len(x))
    elevation -= 35 * np.exp(-(river_distance ** 2) / 18.0)
    vegetation = np.clip(0.25 + 0.75 * np.exp(-((x - center_x) ** 2 + (y - center_y) ** 2) / (2 * (0.34 * size) ** 2)) + rng.normal(0, 0.05, len(x)), 0, 1)
    drainage = np.clip(0.72 - 0.42 * np.exp(-(river_distance ** 2) / 11.0) + rng.normal(0, 0.08, len(x)), 0.05, 1)
    population = rng.poisson(25 + 140 * np.exp(-((x - size * 0.34) ** 2 + (y - size * 0.35) ** 2) / (2 * (0.18 * size) ** 2)))
    vulnerable_fraction = np.clip(0.12 + 0.25 * rng.beta(2, 7, len(x)) + 0.12 * (population > np.quantile(population, 0.82)), 0, 0.65)
    rainfall = np.clip(0.45 + 0.48 * np.exp(-(river_distance ** 2) / 30.0) + rng.normal(0, 0.08, len(x)), 0, 1)
    river_level = np.clip(1.0 - river_distance / (0.45 * size), 0, 1)
    temperature = np.clip(0.45 + 0.35 * (1 - y / size) + rng.normal(0, 0.08, len(x)), 0, 1)
    wind = np.clip(0.25 + 0.55 * (x / size) + rng.normal(0, 0.08, len(x)), 0, 1)
    dryness = np.clip(0.15 + 0.65 * (1 - drainage) + 0.35 * temperature + rng.normal(0, 0.07, len(x)), 0, 1)
    flood_intensity = np.clip(0.40 * rainfall + 0.35 * river_level + 0.25 * (1 - drainage) - 0.18 * (elevation - elevation.min()) / (elevation.max() - elevation.min()), 0, 1)
    wildfire_intensity = np.clip(0.30 * temperature + 0.30 * wind + 0.25 * dryness + 0.15 * vegetation, 0, 1)
    if cfg.scenario == "flood":
        hazard = flood_intensity
    elif cfg.scenario == "wildfire":
        hazard = wildfire_intensity
    else:
        hazard = np.maximum(flood_intensity, wildfire_intensity * 0.88)
    exposure = hazard * np.log1p(population) / np.log1p(max(population.max(), 1))
    vulnerability = exposure * (0.45 + vulnerable_fraction) * (1.1 - drainage)
    return pd.DataFrame({
        "cell_id": [f"C-{int(ix):02d}-{int(iy):02d}" for ix, iy in zip(x, y)],
        "x": x, "y": y, "elevation": elevation, "vegetation": vegetation, "drainage": drainage,
        "population": population, "vulnerable_fraction": vulnerable_fraction,
        "rainfall_index": rainfall, "river_level_index": river_level, "temperature_index": temperature,
        "wind_index": wind, "dryness_index": dryness, "flood_intensity": flood_intensity,
        "wildfire_intensity": wildfire_intensity, "hazard_intensity": hazard,
        "population_exposure": exposure, "vulnerability_score": vulnerability,
    })


def _infrastructure_assets(grid: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    types = ["hospital", "shelter", "power_station", "school", "bridge", "water_pump", "fire_station"]
    criticality = {"hospital": "critical", "shelter": "high", "power_station": "critical", "school": "medium", "bridge": "high", "water_pump": "high", "fire_station": "critical"}
    rows = []
    weighted = grid.sample(n=46, weights=(grid["population"] + 10), random_state=int(rng.integers(0, 100000)))
    for index, row in enumerate(weighted.itertuples(index=False)):
        asset_type = types[index % len(types)]
        capacity = int(rng.integers(40, 280)) if asset_type in {"shelter", "hospital", "school"} else int(rng.integers(1, 6))
        rows.append({
            "asset_id": f"A-{index:03d}", "asset_type": asset_type, "cell_id": row.cell_id,
            "x": int(row.x), "y": int(row.y), "criticality": criticality[asset_type],
            "capacity": capacity, "status": "open", "name": f"{asset_type.replace('_', ' ').title()} {index:02d}",
        })
    return pd.DataFrame(rows)


def _response_resources(grid: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    base_cells = grid.sample(n=8, random_state=int(rng.integers(0, 100000)))
    rows = []
    resource_types = ["rescue_team", "medical_team", "fire_engine", "evac_bus", "water_pump", "supply_truck", "drone_team", "generator"]
    for index, (resource_type, cell) in enumerate(zip(resource_types, base_cells.itertuples(index=False))):
        rows.append({
            "resource_id": f"R-{index:03d}", "resource_type": resource_type, "home_cell": cell.cell_id,
            "x": int(cell.x), "y": int(cell.y), "available_units": int(rng.integers(2, 9)),
            "mobility": float(rng.uniform(0.55, 1.0)), "deployment_cost": float(rng.uniform(1.0, 4.5)),
        })
    return pd.DataFrame(rows)


def _road_links(size: int, grid: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    by_coord = {(int(row.x), int(row.y)): row for row in grid.itertuples(index=False)}
    rows = []
    for y in range(size):
        for x in range(size):
            src = by_coord[(x, y)]
            for dx, dy in [(1, 0), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx >= size or ny >= size:
                    continue
                dst = by_coord[(nx, ny)]
                risk = float(np.clip(0.5 * src.hazard_intensity + 0.5 * dst.hazard_intensity + rng.normal(0, 0.03), 0, 1))
                rows.append({"src_cell": src.cell_id, "dst_cell": dst.cell_id, "distance": 1.0, "road_risk": risk, "is_passable": int(risk < 0.86)})
    return pd.DataFrame(rows)


def _weather_series(cfg: SyntheticDisasterConfig, rng: np.random.Generator) -> pd.DataFrame:
    times = pd.date_range("2026-07-01 00:00:00", periods=72, freq="h", tz="UTC")
    t = np.arange(len(times))
    rainfall = np.clip(0.2 + 0.9 * np.exp(-((t - 30) ** 2) / 150) + rng.normal(0, 0.05, len(t)), 0, 1)
    wind = np.clip(0.25 + 0.55 * np.exp(-((t - 42) ** 2) / 190) + rng.normal(0, 0.06, len(t)), 0, 1)
    temperature = np.clip(0.50 + 0.18 * np.sin(2 * np.pi * t / 24) + 0.25 * np.exp(-((t - 45) ** 2) / 200), 0, 1)
    return pd.DataFrame({"timestamp": times, "rainfall_index": rainfall, "wind_index": wind, "temperature_index": temperature})
