import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_URL = "https://places.googleapis.com/v1/places:searchText"


def find_leads(niche, location, max_results=10):
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_PLACES_API_KEY is not set."
        )

    query = f"{niche} in {location}"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "places.id,"
            "places.displayName,"
            "places.formattedAddress,"
            "places.websiteUri"
        )
    }

    data = {
        "textQuery": query,
        "pageSize": min(max_results, 20)
    }

    response = requests.post(
        GOOGLE_PLACES_URL,
        headers=headers,
        json=data,
        timeout=30
    )

    response.raise_for_status()

    results = response.json().get("places", [])

    leads = []

    for place in results:
        leads.append({
            "business_name": place.get(
                "displayName", {}
            ).get("text", ""),

            "location": place.get(
                "formattedAddress", ""
            ),

            "website": place.get(
                "websiteUri", ""
            ),

            "place_id": place.get("id", "")
        })

    return leads