from disasterintel.synthetic import SyntheticDisasterConfig, generate_synthetic_region


def test_synthetic_region_is_reproducible():
    config = SyntheticDisasterConfig(grid_size=16, seed=7, scenario="combined")
    first = generate_synthetic_region(config)
    second = generate_synthetic_region(config)
    assert first["grid"].equals(second["grid"])
    assert first["assets"].equals(second["assets"])
    assert first["resources"].equals(second["resources"])


def test_synthetic_region_has_expected_layers():
    region = generate_synthetic_region(SyntheticDisasterConfig(grid_size=14, seed=3, scenario="flood"))
    grid = region["grid"]
    assert len(grid) == 14 * 14
    assert {"flood_intensity", "wildfire_intensity", "hazard_intensity", "vulnerability_score"}.issubset(grid.columns)
    assert grid["hazard_intensity"].between(0, 1).all()
    assert len(region["assets"]) > 0
    assert len(region["resources"]) > 0
