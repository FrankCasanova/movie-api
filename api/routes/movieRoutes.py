from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.movieSerializer import MovieResponse
from api.operations.movieOp import get_all_movies, add_movie
from api.db_connection import get_db_session
from typing import Annotated

movie_router = APIRouter()
movie_router.prefix = "/movies"


@movie_router.get("/", response_model=List[MovieResponse])
async def read_movies(session: Annotated[AsyncSession, Depends(get_db_session)]):
    movies = await get_all_movies(session)
    return [
        MovieResponse.model_validate(
            {**movie.__dict__,
             "release_date": movie.release_date.strftime("%d %B %Y")}
            )
        for movie in movies
        ]


@movie_router.post("/")
async def create_movie(movie: MovieResponse, session: Annotated[AsyncSession, Depends(get_db_session)]):
    result = await add_movie(movie, session)
    return result
