FROM ubuntu:20.04
ARG APP_NAME=rick-morty
ARG POETRY_VERSION=1.1.11
ENV APP_NAME=$APP_NAME \
    POETRY_VERSION=$POETRY_VERSION \
    PYTHONPATH="${PYTHONPATH}:/$APP_NAME"
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 \
    python3-pip

WORKDIR /$APP_NAME
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install 
COPY . .
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "rick_morty.main:app"]
