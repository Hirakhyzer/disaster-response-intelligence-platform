# Disaster data boundary

This repository runs immediately with fictional synthetic data. No external dataset is required for the first complete demonstration.

## Synthetic default

Run:

```bash
python scripts/run_synthetic_disaster_lab.py
```

The command generates all needed hazard layers, infrastructure, resources, and weather indices locally.

## Optional future authorized data

Later adapters may use public or authorized sources such as weather forecasts, satellite fire products, hydrology data, open infrastructure records, or open road networks. Any such data must be documented, licensed appropriately, and kept out of Git unless explicitly permitted.

Place real or downloaded data only under:

```text
data/raw/
```

The directory is ignored by Git.

## Minimum fields for future adapters

| Layer | Example fields |
| --- | --- |
| Weather | timestamp, rainfall, temperature, wind |
| Hazard | grid cell or geometry, hazard intensity, confidence |
| Infrastructure | asset ID, type, criticality, location, capacity |
| Population | area ID, population estimate, vulnerable population proxy |
| Resources | resource ID, type, availability, home location |
| Roads | source cell, destination cell, distance, passability, risk |

Do not invent official status or operational authority from incomplete data.
