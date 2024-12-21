from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.movieModels import Movie
from api.schemas.movieSerializer import MovieResponse
from sqlalchemy import exists, select
from api.shared_state import listeners


async def get_all_movies(session: AsyncSession):
    result = await session.execute(select(Movie))
    return result.scalars().all()


async def add_movie(movie: MovieResponse, session: AsyncSession):
    new_movie = Movie(
        title=movie.title,
        poster=movie.poster,
        overview=movie.overview,
        release_date=movie.release_date,
        category=movie.category,
        theater_count=movie.theater_count,
        production_budget=movie.production_budget,
        opening_weekend=movie.opening_weekend,
        legs=movie.legs,
        domestic_share=movie.domestic_share,
        infl_adj_dom_bo=movie.infl_adj_dom_bo
    )
    session.add(new_movie)
    await session.commit()
    for listener in listeners:
        await listener.put(dict(data="New movie added"))
    return {"message": "Movie added successfully"}


# return a movie base on id
async def get_movie_by_id(id: int, session: AsyncSession) -> MovieResponse:
    # Check if ID exists
    exists_query = select(exists().where(Movie.id == id))
    exists_result = await session.execute(exists_query)
    if not exists_result.scalar():
        raise HTTPException(status_code=404, detail="Movie not found")
    # If ID exists, perform the original query
    result = await session.get(Movie, id)
    return MovieResponse.model_validate(result.__dict__)


async def update_movie_op(id, movie: MovieResponse, session: AsyncSession):
    query = select(Movie).where(Movie.id == id)
    result = await session.execute(query)
    existing_movie = result.scalars().first()
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for field in movie.__dict__:
        if field != "id":
            setattr(existing_movie, field, getattr(movie, field))
    session.add(existing_movie)
    await session.commit()
    updated_movie = MovieResponse(**existing_movie.__dict__)
    return updated_movie


async def delete_movie_op(id: int, session: AsyncSession):
    query = select(Movie).where(Movie.id == id)
    result = await session.execute(query)
    existing_movie = result.scalars().first()
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await session.delete(existing_movie)
    await session.commit()
    return {"message": "Movie deleted successfully"}
