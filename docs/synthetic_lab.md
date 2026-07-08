# Synthetic disaster-response laboratory

## Purpose

The synthetic laboratory makes the platform fully runnable without external data. It creates a fictional region, hazard layers, infrastructure, population vulnerability, resources, road links, alerts, maps, resource assignments, route-risk tables, an audit ledger, and an emergency-coordination briefing.

## Command

```bash
python scripts/run_synthetic_disaster_lab.py
```

Optional controls:

```bash
python scripts/run_synthetic_disaster_lab.py --scenario flood --grid-size 36 --seed 42
python scripts/run_synthetic_disaster_lab.py --scenario wildfire --grid-size 36 --seed 42
```

## Outputs

```text
outputs/results/synthetic_grid_hazard.csv
outputs/results/synthetic_infrastructure_assets.csv
outputs/results/synthetic_asset_exposure.csv
outputs/results/synthetic_priority_zones.csv
outputs/results/synthetic_alerts.csv
outputs/results/synthetic_response_resources.csv
outputs/results/synthetic_resource_demand.csv
outputs/results/synthetic_resource_assignments.csv
outputs/results/synthetic_route_risk.csv
outputs/results/synthetic_road_links.csv
outputs/results/synthetic_weather_series.csv
outputs/results/synthetic_disaster_summary.json
outputs/results/audit_ledger.jsonl
outputs/reports/synthetic_disaster_brief.md

outputs/figures/synthetic_hazard_infrastructure_map.png
outputs/figures/synthetic_vulnerability_priority_map.png
outputs/figures/synthetic_resource_allocation_map.png
outputs/figures/synthetic_alert_priority.png
outputs/figures/synthetic_weather_indices.png
```

## Interpretation rules

- Every artifact is synthetic and fictional.
- Figures are planning demonstrations, not official maps.
- Alerts are prioritization examples, not public warnings.
- Assignments are planning recommendations, not dispatch orders.
- Route scores are accessibility evidence, not navigation instructions.
- The project is suitable for research portfolio demonstration, reproducibility, and methodology discussion.
