# Query AI

Query AI is a query application with AI capabilities. It leverages state-of-the-art models for embedding and question answering.

[TOC]

## :white_check_mark: Prerequisites

* **Python 3.13**

* **Poetry** for packaging and dependency management.

  :information_source:See the **appendix** on **installing Poetry** if not yet installed.

* **PostgreSQL** with **vector** extension
  :information_source: See the **appendix** about using Docker to bring up the **PostgreSQL** database, if needed.

* :exclamation: **.env** file with the following syntax in the root of the application:

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

:information_source: Stop the application using `CTRL+C`.

## :book: Usage

### Saving a context to the database
Stores the provided context in the database for later use.

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
Queries the stored context to find answers to the provided question.

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
Answers questions using the context provided in the request and not coming from the database.

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

## :ledger: Logging

The **logging.ini** *(i.e., the configuration)* can be found in the **conf** directory within the **root** of the application. The **default log level** of the **query_ai** package is **INFO** as follows:

```ini
[logger_query_ai]
level=INFO
```

Change the level to `DEBUG` to see more information in the log.

The **name** *(i.e., query_ai.log)* and **location** of the **log file** are indicated in the `handler_fileHandler` configuration as follows:

```ini
[handler_fileHandler]
args=('query_ai.log', 'a', 10485760, 50)
```

## Appendix

### Installing Poetry

Run the following command to install Poetry:

```sh
python -m pip install poetry
```

### PostgreSQL with Vector support in Docker Container

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
poetry run pytest --cov=query_ai --cov-report=html:coverage_report
```

:information_source: The **coverage report** will be in the directory **coverage_report** of the **root** of the application.

## Author

### Ronaldo Webb