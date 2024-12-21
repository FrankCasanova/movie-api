# import asyncontex manager in order to use async sessions
from contextlib import asynccontextmanager
# import base from to create all tables when the app starts
from api.models.movieModels import Base
# import routes
from api.routes.movieRoutes import movie_router
from api.routes.events import event_router
# import db connection
from .db_connection import get_engine
# import the asyncsession class
# import fastapi staff
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# to debug
from icecream import ic
ic.configureOutput(includeContext=True)

# debugpy.listen(("0.0.0.0", 9999))

#TODO: Retrieve a single movie from cache if exist
#TODO: Install Alembic in order to migrate the database


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# add movie routes
app.include_router(movie_router)
app.include_router(event_router)
app.title = "Movie API"
app.version = "0.0.1"
app.summary = "API for movie economic data"
app.description = "Developed by: Frank Casanova \
\n\ncontact: frankcasanova.info@gmail.com \
    \n\non linkedIn: https://www.linkedin.com/in/frankcasanova-/"


# write a basic endpoint to test the api
@app.get("/", tags=["root"])
async def root():
    return {"message": "Movie API please visit /docs"}
