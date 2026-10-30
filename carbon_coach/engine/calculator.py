
from datetime import datetime, timezone
from math import isfinite

from .factors import EMISSION_FACTORS
from google.adk.tools.tool_context import ToolContext


def validate_quantity(value: float, name: str) -> None:
    """Validate that a quantity is a finite, non-negative number."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number.")

    if not isfinite(value):
        raise ValueError(f"{name} must be a finite number.")

    if value < 0:
        raise ValueError(f"{name} cannot be negative.")


def save_activity(tool_context: ToolContext, result: dict) -> None:
    """Save an activity in the current ADK session."""

    activities = list(tool_context.state.get("activities", []))
    activities.append(result)
    tool_context.state["activities"] = activities


def create_result(
    activity: str,
    quantity_name: str,
    quantity: float,
    factor: dict,
    unit: str,
) -> dict:
    """Create a consistent emission calculation result."""

    emissions = quantity * factor["value"]

    return {
        "activity": activity,
        quantity_name: quantity,
        "emissions": round(emissions, 6),
        "unit": unit,
        "factor": factor["value"],
        "factor_source": factor["source"],
        "factor_version": factor["version"],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def calculate_electricity_emissions(
    kwh: float,
    tool_context: ToolContext,
) -> dict:
    """Calculate and save electricity-related CO2 emissions."""

    validate_quantity(kwh, "Electricity usage")

    factor = EMISSION_FACTORS["electricity_india_fy2024_25"]

    result = create_result(
        "electricity", "consumption_kwh", kwh, factor, "kg CO2"
    )
    result["reference_year"] = factor["valid_year"]

    save_activity(tool_context, result)
    return result


def calculate_transport_emissions(
    distance_km: float,
    tool_context: ToolContext,
) -> dict:
    """Calculate and save petrol car travel emissions."""

    validate_quantity(distance_km, "Distance")

    factor = EMISSION_FACTORS["petrol_car_india"]

    result = create_result(
        "transport", "distance_km", distance_km, factor, "kg CO2e"
    )
    result["vehicle"] = factor["vehicle"]

    save_activity(tool_context, result)
    return result


def calculate_food_emissions(
    weight_kg: float,
    tool_context: ToolContext,
) -> dict:
    """Calculate and save rice-related emissions."""

    validate_quantity(weight_kg, "Food weight")

    factor = EMISSION_FACTORS["rice_global"]

    result = create_result(
        "food", "weight_kg", weight_kg, factor, "kg CO2e"
    )
    result["food"] = factor["food"]

    save_activity(tool_context, result)
    return result


def calculate_waste_emissions(
    weight_kg: float,
    tool_context: ToolContext,
) -> dict:
    """Calculate and save organic waste landfill emissions."""

    validate_quantity(weight_kg, "Waste weight")

    factor = EMISSION_FACTORS["organic_waste_landfill_india"]

    result = create_result(
        "waste", "weight_kg", weight_kg, factor, "kg CO2e"
    )
    result["waste_type"] = factor["waste_type"]
    result["treatment"] = factor["treatment"]

    save_activity(tool_context, result)
    return result


def get_activity_history(tool_context: ToolContext) -> dict:
    """Retrieve activities recorded in the current ADK session."""

    activities = tool_context.state.get("activities", [])

    return {
        "total_activities": len(activities),
        "activities": activities,
    }


def get_activity_summary(tool_context: ToolContext) -> dict:
    """Summarize recorded emissions without mixing CO2 and CO2e."""

    activities = tool_context.state.get("activities", [])

    totals = {
        "kg CO2": 0.0,
        "kg CO2e": 0.0,
    }

    category_totals = {}

    for activity in activities:
        unit = activity.get("unit")
        emissions = activity.get("emissions", 0)
        category = activity.get("activity", "unknown")

        if unit not in totals:
            continue

        if (
            isinstance(emissions, bool)
            or not isinstance(emissions, (int, float))
            or not isfinite(emissions)
        ):
            continue

        totals[unit] += emissions

        category_key = f"{category} ({unit})"
        category_totals[category_key] = (
            category_totals.get(category_key, 0.0) + emissions
        )

    return {
        "total_activities": len(activities),
        "emissions_by_unit": {
            unit: round(value, 3)
            for unit, value in totals.items()
        },
        "emissions_by_category": {
            category: round(value, 3)
            for category, value in category_totals.items()
        },
    }

from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo


INDIA_TZ = ZoneInfo("Asia/Kolkata")


def _get_period_summary(
    activities: list,
    start_date: date,
    end_date: date,
) -> dict:
    """Summarize activities within an inclusive date range."""

    totals = {
        "kg CO2": 0.0,
        "kg CO2e": 0.0,
    }

    category_totals = {}
    activity_count = 0
    daily_totals = {}

    for activity in activities:
        timestamp = activity.get("recorded_at")

        if not timestamp:
            continue

        try:
            recorded_at = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

            if recorded_at.tzinfo is None:
                recorded_at = recorded_at.replace(tzinfo=timezone.utc)

            local_date = recorded_at.astimezone(INDIA_TZ).date()

        except (ValueError, TypeError, AttributeError):
            continue

        if not start_date <= local_date <= end_date:
            continue

        unit = activity.get("unit")
        emissions = activity.get("emissions", 0)

        if unit not in totals:
            continue

        if (
            isinstance(emissions, bool)
            or not isinstance(emissions, (int, float))
            or not isfinite(emissions)
        ):
            continue

        category = activity.get("activity", "unknown")

        totals[unit] += emissions
        activity_count += 1

        category_key = f"{category} ({unit})"
        category_totals[category_key] = (
            category_totals.get(category_key, 0.0) + emissions
        )

        if local_date.isoformat() not in daily_totals:
            daily_totals[local_date.isoformat()] = {
                "kg CO2": 0.0,
                "kg CO2e": 0.0,
            }

        daily_totals[local_date.isoformat()][unit] += emissions

    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "timezone": "Asia/Kolkata",
        },
        "total_activities": activity_count,
        "emissions_by_unit": {
            unit: round(value, 3)
            for unit, value in totals.items()
        },
        "emissions_by_category": {
            category: round(value, 3)
            for category, value in category_totals.items()
        },
        "daily_breakdown": {
            day: {
                unit: round(value, 3)
                for unit, value in daily.items()
            }
            for day, daily in sorted(daily_totals.items())
        },
    }


def get_daily_activity_summary(
    tool_context: ToolContext,
    report_date: str = "",
) -> dict:
    """
    Get the activity summary for a date.

    Use YYYY-MM-DD. If no date is provided, use today in India.
    """

    if report_date:
        try:
            selected_date = date.fromisoformat(report_date)
        except ValueError:
            raise ValueError("Use date format YYYY-MM-DD.")
    else:
        selected_date = datetime.now(INDIA_TZ).date()

    activities = tool_context.state.get("activities", [])

    return _get_period_summary(
        activities,
        selected_date,
        selected_date,
    )


def get_weekly_activity_summary(
    tool_context: ToolContext,
    week_start_date: str = "",
) -> dict:
    """
    Get a Monday-to-Sunday weekly activity summary.

    Optionally provide the Monday date in YYYY-MM-DD format.
    """

    if week_start_date:
        try:
            start_date = date.fromisoformat(week_start_date)
        except ValueError:
            raise ValueError("Use date format YYYY-MM-DD.")

        if start_date.weekday() != 0:
            raise ValueError("Week start date must be a Monday.")
    else:
        today = datetime.now(INDIA_TZ).date()
        start_date = today - timedelta(days=today.weekday())

    end_date = start_date + timedelta(days=6)

    activities = tool_context.state.get("activities", [])

    return _get_period_summary(
        activities,
        start_date,
        end_date,
    )
