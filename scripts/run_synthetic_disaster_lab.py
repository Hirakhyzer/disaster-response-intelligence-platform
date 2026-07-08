"""Run the complete synthetic climate and disaster response intelligence lab.

This command creates fictional hazard, infrastructure, population, resource, and
road-network data. It generates planning outputs for research demonstration only;
it does not issue official warnings, dispatch resources, or provide operational
emergency-management instructions.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from disasterintel.alerts import generate_zone_alerts
from disasterintel.config import ensure_output_dirs, set_seed
from disasterintel.exposure import identify_priority_zones, score_asset_exposure, summarize_population_exposure
from disasterintel.ledger import append_record, verify_ledger
from disasterintel.reporting import write_disaster_brief
from disasterintel.resources import allocate_resources, estimate_zone_resource_demand, shelter_capacity_summary
from disasterintel.routes import score_resource_routes
from disasterintel.synthetic import SyntheticDisasterConfig, generate_synthetic_region
from disasterintel.visualization import plot_alert_priority, plot_hazard_map, plot_resource_allocations, plot_vulnerability_map, plot_weather_series


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic climate/disaster response intelligence laboratory.")
    parser.add_argument("--grid-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--scenario", choices=["flood", "wildfire", "combined"], default="combined")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    set_seed(args.seed)
    region = generate_synthetic_region(SyntheticDisasterConfig(grid_size=args.grid_size, seed=args.seed, scenario=args.scenario))
    grid = region["grid"]
    assets = region["assets"]
    resources = region["resources"]
    roads = region["roads"]
    weather = region["weather"]

    exposed_assets = score_asset_exposure(grid, assets)
    priority_zones = identify_priority_zones(grid, top_n=14)
    alerts = generate_zone_alerts(priority_zones, exposed_assets)
    resource_demand = estimate_zone_resource_demand(priority_zones)
    assignments = allocate_resources(priority_zones, resources)
    routes = score_resource_routes(resources, assignments, roads)
    population_summary = summarize_population_exposure(grid)
    shelter_summary = shelter_capacity_summary(exposed_assets, grid)

    outputs = ensure_output_dirs(args.output_dir)
    grid.to_csv(outputs["results"] / "synthetic_grid_hazard.csv", index=False)
    assets.to_csv(outputs["results"] / "synthetic_infrastructure_assets.csv", index=False)
    exposed_assets.to_csv(outputs["results"] / "synthetic_asset_exposure.csv", index=False)
    priority_zones.to_csv(outputs["results"] / "synthetic_priority_zones.csv", index=False)
    alerts.to_csv(outputs["results"] / "synthetic_alerts.csv", index=False)
    resources.to_csv(outputs["results"] / "synthetic_response_resources.csv", index=False)
    resource_demand.to_csv(outputs["results"] / "synthetic_resource_demand.csv", index=False)
    assignments.to_csv(outputs["results"] / "synthetic_resource_assignments.csv", index=False)
    routes.to_csv(outputs["results"] / "synthetic_route_risk.csv", index=False)
    roads.to_csv(outputs["results"] / "synthetic_road_links.csv", index=False)
    weather.to_csv(outputs["results"] / "synthetic_weather_series.csv", index=False)

    plot_hazard_map(grid, exposed_assets, outputs["figures"] / "synthetic_hazard_infrastructure_map.png")
    plot_vulnerability_map(grid, priority_zones, outputs["figures"] / "synthetic_vulnerability_priority_map.png")
    plot_resource_allocations(grid, resources, assignments, outputs["figures"] / "synthetic_resource_allocation_map.png")
    plot_alert_priority(alerts, outputs["figures"] / "synthetic_alert_priority.png")
    plot_weather_series(weather, outputs["figures"] / "synthetic_weather_indices.png")

    ledger_path = outputs["results"] / "audit_ledger.jsonl"
    append_record(ledger_path, {
        "experiment": "synthetic_disaster_lab",
        "seed": args.seed,
        "scenario": args.scenario,
        "grid_size": args.grid_size,
        "grid_cells": int(len(grid)),
        "asset_count": int(len(assets)),
        "resource_count": int(len(resources)),
        "population_summary": population_summary,
        "shelter_summary": shelter_summary,
        "boundary": "Synthetic research planning only; not an official warning, route, evacuation, or dispatch system.",
    })
    summary = {
        "data_origin": "synthetic fictional disaster-response region",
        "seed": args.seed,
        "scenario": args.scenario,
        "grid_size": args.grid_size,
        "grid_cells": int(len(grid)),
        "asset_count": int(len(assets)),
        "resource_count": int(len(resources)),
        "alert_count": int(len(alerts)),
        "population_summary": population_summary,
        "shelter_summary": shelter_summary,
        "ledger": verify_ledger(ledger_path),
        "human_control_boundary": "All recommendations require official emergency-management review; no public warning, evacuation, road closure, or dispatch action is issued.",
    }
    (outputs["results"] / "synthetic_disaster_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    write_disaster_brief(outputs["reports"] / "synthetic_disaster_brief.md", summary, population_summary, alerts, assignments)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
