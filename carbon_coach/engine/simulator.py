
from math import isfinite

from .factors import EMISSION_FACTORS


def simulate_transport_change(
    distance_km: float,
    alternative_factor_id: str,
) -> dict:
    """
    Compare petrol car emissions with a registered transport factor.

    Both factors must use the same unit and gas measurement basis.
    """

    # Validate distance
    if (
        isinstance(distance_km, bool)
        or not isinstance(distance_km, (int, float))
    ):
        raise ValueError("Distance must be a number.")

    if not isfinite(distance_km) or distance_km < 0:
        raise ValueError(
            "Distance must be a finite, non-negative number."
        )

    # Validate alternative factor
    if alternative_factor_id not in EMISSION_FACTORS:
        raise ValueError("Unknown emission factor.")

    current = EMISSION_FACTORS["petrol_car_india"]
    alternative = EMISSION_FACTORS[alternative_factor_id]

    if alternative.get("category") != "transport":
        raise ValueError(
            "Alternative must be a transport factor."
        )

    if alternative.get("unit") != current.get("unit"):
        raise ValueError(
            "Emission factor units must match."
        )

    if alternative.get("gas_basis") != current.get("gas_basis"):
        raise ValueError(
            "Gas measurement bases must match."
        )

    # Calculate emissions
    current_emissions = distance_km * current["value"]
    alternative_emissions = distance_km * alternative["value"]

    savings = current_emissions - alternative_emissions

    return {
        "distance_km": distance_km,
        "current_vehicle": current["vehicle"],
        "alternative_factor_id": alternative_factor_id,
        "current_emissions_kg_co2e": round(
            current_emissions, 3
        ),
        "alternative_emissions_kg_co2e": round(
            alternative_emissions, 3
        ),
        "potential_savings_kg_co2e": round(
            savings, 3
        ),
        "alternative_factor": alternative["value"],
        "alternative_factor_source": alternative["source"],
        "alternative_factor_version": alternative["version"],
    }
