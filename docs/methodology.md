# Methodology

## Scope and operational boundary

This repository is a synthetic-first climate and disaster response intelligence research platform. It supports scenario modelling, map generation, exposure analysis, resource planning, route-risk scoring, and evidence-based briefings.

It is **not** an official warning system, dispatch tool, evacuation-order generator, satellite product, hydrological model, fire-spread model, or public-safety authority. Any real-world use would require official data feeds, validation, legal authority, operational review, and emergency-management approval.

## 1. Synthetic scenario layers

The default laboratory creates a fictional gridded region with:

- elevation proxy;
- drainage proxy;
- vegetation proxy;
- population and vulnerable-population fraction;
- rainfall, river-level, temperature, wind, and dryness indices;
- infrastructure assets;
- response resource pools;
- road links and passability.

These are simulation variables, not observations.

## 2. Hazard modelling

Flood intensity is a transparent weighted combination of rainfall, river-level proximity, drainage stress, and elevation. Wildfire intensity combines temperature, wind, dryness, and vegetation. A combined scenario takes the larger of flood and scaled wildfire pressure.

The formulas are interpretable research heuristics. They do not replace hydrological, hydraulic, meteorological, or fire-behavior models.

## 3. Exposure and vulnerability

Population exposure combines hazard intensity with population density. Vulnerability further weights the exposed population by vulnerable-population fraction and drainage constraints. Infrastructure assets are scored by local hazard, local vulnerability, and asset criticality.

Asset exposure bands are used for prioritization and briefing, not official damage estimates.

## 4. Alert prioritization

Priority-zone alerts combine hazard intensity, vulnerability score, population, nearby critical infrastructure, and confidence. Each alert includes an evidence-oriented recommended focus. Alerts are ranked for analyst or emergency-management review.

Alert output is a decision-support artifact, not a public alert or evacuation notice.

## 5. Resource allocation

The resource planner estimates demand for rescue, medical, fire, evacuation, pump, supply, drone, and generator resources. It assigns available resource pools to high-priority zones using zone score, population need, flood/wildfire fit, distance, mobility, and deployment cost.

The result is a planning recommendation. It must be approved, changed, or rejected by authorized incident command.

## 6. Route-risk scoring

Road links have hazard-influenced risk and a passability flag. The route module builds a graph over passable links and calculates shortest risk-adjusted path cost from resource base to assigned zone. Missing routes are reported explicitly.

This is not turn-by-turn navigation or official road-closure information.

## 7. Auditability

Every synthetic run writes CSV result tables, figures, a local briefing, and a hash-chained audit ledger containing seed, scenario, grid size, exposure summary, shelter summary, and safety boundary.

## 8. Limitations

- Synthetic hazard layers are not physically calibrated.
- Population and infrastructure records are fictional.
- Road-risk and resource assignment are simplified heuristics.
- No official forecast, satellite, hydrology, wildfire, public warning, or road data are ingested by default.
- Recommendations require official human review before action.
