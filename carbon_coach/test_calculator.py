from carbon_coach.engine.simulator import simulate_transport_change


def test_transport_simulation():
    result = simulate_transport_change(
        distance_km=20,
        alternative_factor_id="petrol_car_india"
    )

    assert result["current_emissions_kg_co2e"] == 3.06
    assert result["alternative_emissions_kg_co2e"] == 3.06
    assert result["potential_savings_kg_co2e"] == 0.0