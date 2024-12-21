from pydantic import BaseModel, Field
from datetime import date


class MovieResponse(BaseModel):
    id: int = Field(..., title="Movie ID", examples=[1])
    title: str = Field(..., title="Movie Title", max_length=100, min_length=1, examples=["The Shawshank Redemption"])
    poster: str = Field(..., title="Poster", max_length=1000, min_length=1, examples=["https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg"])
    overview: str = Field(..., title="Overview", max_length=1000, min_length=1, examples=["Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."])
    release_date: date = Field(..., title="Release Date", format="date")
    category: str = Field(..., title="Category", max_length=100, min_length=1, examples=["Drama"])
    theater_count: int = Field(..., title="")
    production_budget: int = Field(..., title="Amount of money for production budget", examples=["543555100"])
    opening_weekend: int = Field(..., title="Amount of money for opening weekend", examples=["100000000"])
    legs: float = Field(..., title="movie's ability to sustain its box office performance over time", examples=["0.5"])
    domestic_share: float = Field(..., title="This refers to the percentage of the movie's worldwide box office total that came from the domestic (US and Canada) market.", examples=["45.2"])
    infl_adj_dom_bo: int = Field(..., title="This refers to the domestic box office total adjusted for inflation.", examples=["233444897"])



    class Config:
        from_atributes = True


class UpdateMovieFieldRequest(BaseModel):
    field_name: str
    new_value: str
