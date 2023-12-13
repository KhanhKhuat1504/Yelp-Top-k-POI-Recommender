from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_location_by_address(address: str):
    
    # Init Nominatim API
    geolocator = Nominatim(user_agent='this_user')

    try:
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude) if location else (None, None)
    except GeocoderTimedOut:
        return None
    
def calculate_distance_score(poi_distance, max_distance):
    # Inverse score based on distance 
    # d = 0 if out of max_distance
    # 0 < d <= 1 if within the max_distance radius from the poi
    return max(0, (max_distance-poi_distance)/max_distance)
