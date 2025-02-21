# Query AI

## Description
Query AI is a query application with AI capabilities. It leverages state-of-the-art models for embedding and question answering.

[TOC]

## Prerequisites

* **Python 3.13**
* **Poetry** for packaging and dependency management
* **Postgres** with **vector** extension
* **.env** file with the following syntax in the root of the application:

  ```properties
  # The name of the database to connect to
  QA_DB_NAME=<DATABASE_NAME>

  # The host address of the database
  QA_DB_HOST=<HOSTNAME>

  # The port number to connect to the database
  QA_DB_PORT=<DATABASE_PORT>

  # The username used to authenticate with the database
  QA_DB_USERNAME=<DATABASE_USERNAME>

  # The password used to authenticate with the database
  QA_DB_PASSWORD=<DATABASE_PASSWORD>
  ```

  Example:

  ```properties
  QA_DB_NAME=query-ai
  QA_DB_HOST=localhost
  QA_DB_PORT=5432
  QA_DB_USERNAME=postgres
  QA_DB_PASSWORD=mypassword
  ```

## Installation

Run the following command at the **root** of the application to download the dependencies:

```sh
poetry install
```

## Running the Application

Run the application using the following command at the **root** of the application:

```sh
poetry run app
```

Expect something like the following:

```
2025-02-22 01:36:01,784 - query_ai.application - INFO - Query AI application
```

After this, the application will be listening on port **5000**.

## Usage

### Saving a context to the database

#### Endpoint

`[PUT]` http://localhost:5000/api/v1/context

#### JSON Payload

```json
{
    "context": "<CONTEXT>"
}
```

**Example:**

```json
{
    "context": "The quick brown fox jumps over the lazy dog."
}
```

### Asking a question based on the context in the database

If the payload doesn't have context, the context will be retrieved from the database.

#### Endpoint

`[POST]` http://localhost:5000/api/v1/query

#### JSON Payload

```json
{
    "question": "<QUESTION>"
}
```

**Example:**

```json
{
    "question": "What jumps over the lazy dog?"
}
```

### Asking a question from a provided context

If the payload has context, the question will be answered based on the provided context without using the database.

#### Endpoint

`[POST]` http://localhost:5000/api/v1/query

#### JSON Payload

```json
{
    "context": "<CONTEXT>",
    "question": "<QUESTION>"
}
```

**Example:**

```json
{
    "context": "The sun is in the center of the solar system.",
    "question": "What is in the center of the solar system?"
}
```

## Appendix

### Postgres with Vector support in Docker Container

Run the following command from the **root** of the application:

```sh
docker compose up
```

### Running a static code analyzer

Run the following command from the **root** of the application:

```sh
poetry run lint
```

### Running the unit tests

Run the following command from the **root** of the application:

```sh
poetry run pytest
```

## Author

Ronaldo Webb