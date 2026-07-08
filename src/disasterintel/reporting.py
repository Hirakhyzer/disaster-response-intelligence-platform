"""Local briefing generation for synthetic disaster-response experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def write_disaster_brief(
    path: str | Path,
    summary: dict[str, Any],
    population_summary: dict[str, Any],
    alerts: pd.DataFrame,
    assignments: pd.DataFrame,
) -> None:
    """Write a concise local markdown briefing with explicit research boundary."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Climate and Disaster Response Intelligence Brief",
        "",
        "> **Synthetic research warning:** this briefing is generated from fictional synthetic data. It is not an official alert, warning, evacuation order, or dispatch instruction.",
        "",
        "## Run summary",
        "",
        f"- Scenario: `{summary['scenario']}`",
        f"- Seed: `{summary['seed']}`",
        f"- Grid cells: `{summary['grid_cells']}`",
        f"- Infrastructure assets: `{summary['asset_count']}`",
        f"- Response resource pools: `{summary['resource_count']}`",
        f"- Ledger valid: `{summary['ledger']['valid']}`",
        "",
        "## Population exposure",
        "",
        f"- Total fictional population: `{population_summary['total_population']}`",
        f"- Exposed population: `{population_summary['exposed_population']}`",
        f"- Severe-hazard population: `{population_summary['severe_hazard_population']}`",
        f"- Estimated vulnerable exposed population: `{population_summary['estimated_vulnerable_exposed_population']}`",
        "",
        "## Highest-priority alerts",
        "",
        "| Alert | Cell | Severity | Score | Focus |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in alerts.head(10).itertuples(index=False):
        lines.append(f"| {row.alert_id} | {row.cell_id} | {row.severity} | {row.priority_score:.2f} | {row.recommended_focus} |")
    lines.extend(["", "## Resource recommendations", "", "| Resource | Assigned cell | Units | Route note |", "| --- | --- | ---: | --- |"])
    for row in assignments.itertuples(index=False):
        lines.append(f"| {row.resource_type} | {row.assigned_cell} | {row.recommended_units} | Planning recommendation only |")
    lines.extend([
        "",
        "## Human-control boundary",
        "",
        "All recommendations require official emergency-management review. The software does not issue public warnings, evacuation orders, dispatch orders, or route closures.",
    ])
    destination.write_text("\n".join(lines), encoding="utf-8")
