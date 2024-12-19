# create a movie model for the database
from sqlalchemy import Column, Integer, String, Float, Date, BigInteger
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    poster = Column(String, nullable=False)
    overview = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    theater_count = Column(BigInteger, nullable=False)
    production_budget = Column(BigInteger, nullable=False)
    opening_weekend = Column(BigInteger, nullable=False)
    legs = Column(Float, nullable=False)
    domestic_share = Column(Float, nullable=False)
    infl_adj_dom_bo = Column(BigInteger, nullable=False)
