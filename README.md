# crud-api repo
CRUD python API for SQL, using FastAPI.

## How the API works:

## About this project:
- Serves as a sample of the implementation of a CRUD API using FastAPI and PostgreSQL, in a dockerized environment.
- This API will allow you to perform Create, Read, Update, and Delete operations on a PostgreSQL database using FastAPI.
- [Optional] If you're in windows: install [`ngrok`](https://ngrok.com/download/windows), sign in, then you can expose your local API to the internet for testing.


## Setup for this project:

1. **Docker Setup:** Ensure you have [Docker](https://www.docker.com/products/docker-desktop/) installed and running on your machine.
2. **Clone the Repository**
3. **Run** `$ docker-compose up --build` (use `-d` to run in detached mode)
    3.1 [Optional]: On any change on the database initialization file (`db/init.sql`), run `$ docker compose down -v` first do destroy the volumes before restarting.

