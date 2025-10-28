from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with hits, misses, and hit ratio.
    """
    try:
        # Connect to Redis through django-redis
        redis_conn = get_redis_connection("default")

        # Fetch Redis INFO stats
        info = redis_conn.info()

        # Extract hits and misses
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Calculate hit ratio using total_requests
        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        # Log metrics
        logger.info(f"Redis Cache Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2%}")

        # Return structured data
        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 4)
        }

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0.0
        }
