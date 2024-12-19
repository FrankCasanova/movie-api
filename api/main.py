#import asyncontex manager in order to use async sessions
from contextlib import asynccontextmanager
from datetime  import datetime
#import base from to create all tables when the app starts
from .models import Base, Movie
#import db connection
from .db_connection import get_engine, get_db_session
#import the asyncsession class
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
#import fastapi staff
from fastapi import FastAPI, Depends


#to debug
from icecream import ic
from pydantic import BaseModel, field_validator

ic.configureOutput(includeContext=True)



@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    lifespan=lifespan, 
    root_path='/api'
    )

#write a basic endpoint to test the api
@app.get("/")
async def root():
    return {"message": "Hello World"}


class MovieResponse(BaseModel):
    title: str
    poster: str
    overview: str
    release_date: str
    category: str
    theater_count: int
    production_budget: int
    opening_weekend: int
    legs: float
    domestic_share: float
    infl_adj_dom_bo: int
    
    

    @field_validator('release_date')
    def parse_release_date(cls, v):
        try:
            return datetime.strptime(v, "%d %B %Y").date()
        except ValueError:
            raise ValueError("Invalid release date format. Please use '2 July 1991'.")
    
    
    class Config:
        orm_mode = True

# endpoint to add movies to the database
@app.post("/movies")
async def add_movie(movie: MovieResponse, session: AsyncSession = Depends(get_db_session)):
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

@app.get("/movies", response_model=list[MovieResponse])
async def get_movies(session: AsyncSession = Depends(get_db_session)):
    movies = await session.execute(select(Movie))
    movies = movies.scalars().all()
    movie_responses = [
        MovieResponse.model_validate(
            {**movie.__dict__,
             "release_date": movie.release_date.strftime("%d %B %Y")}
            )
        for movie in movies
        ]
    return movie_responses