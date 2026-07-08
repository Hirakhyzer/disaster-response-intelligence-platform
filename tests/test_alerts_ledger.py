from pathlib import Path

from disasterintel.alerts import generate_zone_alerts
from disasterintel.exposure import identify_priority_zones, score_asset_exposure
from disasterintel.ledger import append_record, verify_ledger
from disasterintel.synthetic import SyntheticDisasterConfig, generate_synthetic_region


def test_alert_generation_creates_ranked_scores():
    region = generate_synthetic_region(SyntheticDisasterConfig(grid_size=16, seed=21, scenario="wildfire"))
    exposed_assets = score_asset_exposure(region["grid"], region["assets"])
    zones = identify_priority_zones(region["grid"], top_n=5)
    alerts = generate_zone_alerts(zones, exposed_assets)
    assert len(alerts) == 5
    assert alerts["priority_score"].is_monotonic_decreasing
    assert alerts["severity"].isin(["watch", "moderate", "high", "critical"]).all()


def test_audit_ledger_verifies(tmp_path: Path):
    ledger = tmp_path / "audit.jsonl"
    append_record(ledger, {"experiment": "unit", "seed": 1})
    append_record(ledger, {"experiment": "unit", "seed": 2})
    status = verify_ledger(ledger)
    assert status["valid"]
    assert status["records"] == 2
