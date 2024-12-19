from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.movieModels import Movie
from api.schemas.movieSerializer import MovieResponse, UpdateMovieFieldRequest
from api.operations.movieOp import get_all_movies, add_movie, get_movie_by_id, update_movie_op, delete_movie_op
from api.db_connection import get_db_session
from typing import Annotated

movie_router = APIRouter()
movie_router.prefix = "/movies"


@movie_router.get("/", response_model=List[MovieResponse], tags=["movies"])
async def read_movies(session: Annotated[AsyncSession, Depends(get_db_session)]):
    movies = await get_all_movies(session)
    return movies


@movie_router.post("/", response_model=dict, tags=["movies"])
async def create_movie(movie: MovieResponse, session: Annotated[AsyncSession, Depends(get_db_session)]):
    result = await add_movie(movie, session)
    return result

#router to return movie by id
@movie_router.get("/{id}", response_model=MovieResponse, tags=["movies"])
async def get_movie(id: int, session: Annotated[AsyncSession, Depends(get_db_session)]):
    try:
        return await get_movie_by_id(id, session)
    except HTTPException as e:
        raise e
    

@movie_router.put("/{id}", response_model=MovieResponse, tags=["movies"])
async def update_movie(id: int, movie: MovieResponse, session: AsyncSession = Depends(get_db_session)):
    updated_movie = await update_movie_op(id, movie, session)
    return updated_movie

@movie_router.delete("/{id}", response_model=dict, tags=["movies"])
async def delete_movie(id: int, session: AsyncSession = Depends(get_db_session)):
    result = await delete_movie_op(id, session)
    return result