from sqlalchemy.ext.asyncio import AsyncSession
from api.models.movieModels import Movie
from api.schemas.movieSerializer import MovieResponse
from sqlalchemy import select


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
    return {"message": "Movie added successfully"}
