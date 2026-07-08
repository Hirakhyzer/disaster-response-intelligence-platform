from disasterintel.exposure import identify_priority_zones, score_asset_exposure, summarize_population_exposure
from disasterintel.resources import allocate_resources, estimate_zone_resource_demand, shelter_capacity_summary
from disasterintel.routes import score_resource_routes
from disasterintel.synthetic import SyntheticDisasterConfig, generate_synthetic_region


def test_exposure_and_resource_pipeline_runs():
    region = generate_synthetic_region(SyntheticDisasterConfig(grid_size=16, seed=11, scenario="combined"))
    exposed_assets = score_asset_exposure(region["grid"], region["assets"])
    priority_zones = identify_priority_zones(region["grid"], top_n=6)
    demand = estimate_zone_resource_demand(priority_zones)
    assignments = allocate_resources(priority_zones, region["resources"])
    routes = score_resource_routes(region["resources"], assignments, region["roads"])
    population = summarize_population_exposure(region["grid"])
    shelters = shelter_capacity_summary(exposed_assets, region["grid"])
    assert exposed_assets["asset_exposure_score"].between(0, 100).all()
    assert len(priority_zones) == 6
    assert not demand.empty
    assert len(assignments) == len(region["resources"])
    assert len(routes) == len(assignments)
    assert population["total_population"] >= population["exposed_population"]
    assert shelters["capacity_coverage_fraction"] >= 0
