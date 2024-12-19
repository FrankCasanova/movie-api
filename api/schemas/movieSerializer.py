from pydantic import BaseModel, field_validator
from datetime import datetime


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
