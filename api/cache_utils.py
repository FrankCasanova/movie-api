# cache_utils.py
import json
from typing import List
from icecream import ic
from redis.asyncio import Redis
from api.models.movieModels import Movie

CACHE_KEY = "all_movies"
CACHE_EXPIRATION = 3600  # 1 hour in seconds


def movie_serializer(movie: Movie) -> dict:
    """Serialize a movie object to dict for caching"""
    return {
        "id": movie.id,
        "title": movie.title,
        "poster": movie.poster,
        "overview": movie.overview,
        "release_date": movie.release_date.isoformat(),
        "category": movie.category,
        "theater_count": movie.theater_count,
        "production_budget": movie.production_budget,
        "opening_weekend": movie.opening_weekend,
        "legs": movie.legs,
        "domestic_share": movie.domestic_share,
        "infl_adj_dom_bo": movie.infl_adj_dom_bo
    }


async def get_cached_movies(redis: Redis) -> List[dict] | None:
    """Retrieve movies from cache if they exist"""
    try:
        cached_data = await redis.get(CACHE_KEY)
        if cached_data:
            try:
                return json.loads(cached_data.decode('utf-8'))
            except UnicodeDecodeError:
                return json.loads(cached_data)
    except Exception as e:
        ic(e)
    return None


async def set_cached_movies(redis: Redis, movies: List[Movie]) -> None:
    """Store movies in cache"""
    try:
        serialized_movies = [movie_serializer(movie) for movie in movies]
        json_str = json.dumps(serialized_movies)

        await redis.set(
            CACHE_KEY,
            json_str,
            ex=CACHE_EXPIRATION  # Set cache expiration
        )
    except Exception as e:
        ic(e)


async def delete_cached_movies(redis: Redis) -> None:
    try:
        await redis.delete(CACHE_KEY)
    except Exception:
        pass
