from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Fetch all properties from cache if available.
    Otherwise, query the database and cache the results for 1 hour.
    """
    # Try to get cached data
    properties = cache.get('all_properties')

    if properties is not None:
        print("Returning properties from cache...")
        return properties

    # Not in cache: fetch from DB
    print("Fetching properties from database...")
    properties = list(Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    ))

    # Cache the data for 1 hour (3600 seconds)
    cache.set('all_properties', properties, 3600)

    return properties
