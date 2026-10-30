
"""
Carbon Coach - Emission Factor Registry

Sources:
Central Electricity Authority (CEA), India.
CO2 Baseline Database, Version 21.0.
FY 2024-25.
"""

EMISSION_FACTORS = {
    "electricity_india_fy2024_25": {
        "category": "electricity",
        "value": 0.710,
        "unit": "kg CO2/kWh",
        "gas_basis": "CO2_only",
        "region": "India",
        "valid_year": "FY 2024-25",
        "source": "Central Electricity Authority (CEA)",
        "dataset": "CO2 Baseline Database",
        "version": "21.0",
        "source_url": (
            "https://cea.nic.in/cdm-co2-baseline-database/"
        )
    },

    "petrol_car_india": {
        "category": "transport",
        "vehicle": "Petrol sedan below 1600 cc",
        "value": 0.153,
        "unit": "kg CO2e/km",
        "gas_basis": "CO2e",
        "region": "India",
        "source": "India GHG Program",
        "dataset": "Transport emission factors",
        "version": "Reference factor",
        "source_url": (
            "https://bsmedia.business-standard.com/_media/bs/data/announcements/bse/11122025/bcc88fd7-ac12-445a-801e-f13d1c816ace.pdf"
        )
    },

    "rice_global": {
        "category": "food",
        "food": "Rice",
        "value": 4.45,
        "unit": "kg CO2e/kg",
        "gas_basis": "CO2e",
        "region": "Global average",
        "reference_year": "2010",
        "source": "Our World in Data",
        "dataset": "Poore & Nemecek (2018)",
        "version": "2018 study, OWID dataset",
        "source_url": (
            "https://ourworldindata.org/grapher/ghg-per-kg-poore"
        )
    },

    "organic_waste_landfill_india": {
        "category": "waste",
        "waste_type": "Organic waste",
        "treatment": "Landfill",
        "value": 1.29,
        "unit": "kg CO2e/kg",
        "gas_basis": "CO2e",
        "region": "India",
        "source": "Ministry of Environment, Forest and Climate Change",
        "dataset": "Low-Carbon Lifestyles",
        "version": "2019 report",
        "source_url": (
            "https://www.moef.gov.in/uploads/2019/10/LOW-CARBON-LIFESTYLES.pdf"
        )
    }
}
