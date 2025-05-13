from hestia_earth.aggregation.utils.weights import _country_irrigated_weight


def test_irrigated_weight():
    country_id = 'GADM-ECU'
    assert round(_country_irrigated_weight(country_id, 2010, 2019), 2) == 0.07
