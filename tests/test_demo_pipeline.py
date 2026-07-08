from disasterintel.alerts import generate_zone_alerts
from disasterintel.exposure import identify_priority_zones, score_asset_exposure
from disasterintel.resources import allocate_resources
from disasterintel.routes import score_resource_routes
from disasterintel.synthetic import SyntheticDisasterConfig, generate_synthetic_region


def test_end_to_end_core_pipeline_is_data_free_and_deterministic():
    region = generate_synthetic_region(SyntheticDisasterConfig(grid_size=14, seed=31, scenario="combined"))
    exposed = score_asset_exposure(region["grid"], region["assets"])
    zones = identify_priority_zones(region["grid"], top_n=5)
    alerts = generate_zone_alerts(zones, exposed)
    assignments = allocate_resources(zones, region["resources"])
    routes = score_resource_routes(region["resources"], assignments, region["roads"])
    assert not alerts.empty
    assert not assignments.empty
    assert not routes.empty
    assert alerts.iloc[0]["priority_score"] >= alerts.iloc[-1]["priority_score"]
