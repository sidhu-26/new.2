from rest_framework.response import Response #type: ignore
from rest_framework.decorators import api_view #type: ignore
import requests #type: ignore
from .models import studios
from math import radians, cos, sin, asin, sqrt

def harvesine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  
    return c * r

@api_view(['GET'])
def nearest_std(request):
    try:
        user_latitude = float(request.GET.get('latitude'))
        user_longitude = float(request.GET.get('longitude'))
    except (TypeError, ValueError):
        return Response({'error': 'Check latitude and longitude values.'}, status=400)

    SerpApiKey = "" # use a p i key , (key available in readme)
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_maps",
        "q": "dance studio",
        "ll": f"@{user_latitude},{user_longitude},15z",
        "location": f"{user_latitude},{user_longitude}",
        "google_domain": "google.co.in",
        "radius": 4000,
        "api_key": SerpApiKey
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "local_results" not in data or not data["local_results"]:
        return Response({"error": "No dance studios found near your location."}, status=404)

    studios = [
        {
            "name": studio["title"],
            "address": studio.get("address", "Address not available"),
            "rating": studio.get("rating", "Not available"),
            "distance_KM": round(harvesine(
                user_latitude, user_longitude,
                studio["gps_coordinates"]["latitude"],
                studio["gps_coordinates"]["longitude"]
            ), 2)
        }
        for studio in data["local_results"]
    ]

    filtered_studios = [studio for studio in studios if studio["distance_KM"] <= 4]

    filtered_studios.sort(key=lambda x: x['distance_KM'])

    return Response({"studios": filtered_studios})
