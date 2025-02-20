# Query AI

## Description
Query AI is a query application with AI capabilities. It leverages state-of-the-art models for embedding and question answering.

## Installation
To install the required dependencies, use [Poetry](https://python-poetry.org/):

```sh
poetry install
```

## Usage
To run the application, use the following commands:

```sh
poetry run pytest
poetry run python -m query_ai.application
poetry build
```

Create a `.env` file with the following content:

```sh
QA_DB_NAME=query-ai
QA_DB_HOST=localhost
QA_DB_PORT=5432
QA_DB_USERNAME=postgres
QA_DB_PASSWORD=mypassword
```

## Project Structure
- `pyproject.toml`: Configuration file for Poetry.
- `query_ai/model/ModelMgr.py`: Contains the `ModelMgr` class for managing models.

## Dependencies
- Python 3.13
- Transformers 4.48.3
- Torch 2.6.0
- pgvector 0.3.6
- psycopg2 2.9.10
- nltk 3.9.1

## Development Dependencies
- Cython 3.0.11
- Pytest 8.3.4

## Author
Ron Webb <ron@ronella.xyz>
