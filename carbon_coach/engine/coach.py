
from google.adk.tools.tool_context import ToolContext


def get_reduction_recommendations(
    tool_context: ToolContext,
) -> dict:
    """
    Generate recommendations based on activities recorded
    in the current ADK session.
    """

    activities = tool_context.state.get("activities", [])

    if not activities:
        return {
            "message": (
                "No activities recorded yet. "
                "Log some activities to receive personalized suggestions."
            ),
            "recommendations": [],
        }

    recommendations = []
    category_totals = {}

    for activity in activities:
        category = activity.get("activity")
        unit = activity.get("unit")
        emissions = activity.get("emissions", 0)

        if category not in {
            "electricity", "transport", "food", "waste"
        }:
            continue

        if unit not in {"kg CO2", "kg CO2e"}:
            continue

        if isinstance(emissions, bool) or not isinstance(
            emissions, (int, float)
        ):
            continue

        key = (category, unit)
        category_totals[key] = (
            category_totals.get(key, 0.0) + emissions
        )

    suggestions = {
        "electricity": {
            "suggestion": (
                "Switch off unused lights, fans and appliances. "
                "Consider energy-efficient appliances."
            ),
            "action": (
                "Track your electricity consumption and compare "
                "usage across days."
            ),
        },
        "transport": {
            "suggestion": (
                "Consider public transport, carpooling, cycling "
                "or walking for suitable journeys."
            ),
            "action": (
                "Look for short journeys where you can avoid "
                "using a petrol car."
            ),
        },
        "food": {
            "suggestion": (
                "Plan meals carefully and avoid unnecessary "
                "food waste."
            ),
            "action": (
                "Track food quantities and consider reducing "
                "avoidable food waste."
            ),
        },
        "waste": {
            "suggestion": (
                "Separate organic waste and consider composting "
                "where suitable facilities are available."
            ),
            "action": (
                "Check whether your campus or community provides "
                "organic waste collection or composting."
            ),
        },
    }

    for (category, unit), emissions in category_totals.items():
        recommendation = suggestions[category]

        recommendations.append({
            "category": category,
            "recorded_emissions": round(emissions, 3),
            "unit": unit,
            "suggestion": recommendation["suggestion"],
            "action": recommendation["action"],
        })

    return {
        "message": (
            "Recommendations generated from your recorded activities. "
            "These are practical suggestions, not calculated savings."
        ),
        "categories_analyzed": len(recommendations),
        "recommendations": recommendations,
    }
