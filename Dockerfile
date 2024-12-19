FROM python:3.12-slim-bullseye

WORKDIR /code

#install Git and other necessary packages
RUN apt-get update && apt-get install -y git

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the uv configuration file and requirements
COPY uv.toml requirements.txt ./

# Install dependencies using uv
RUN uv pip install --system -r requirements.txt

# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
