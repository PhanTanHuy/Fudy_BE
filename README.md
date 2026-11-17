# FastAPI Backend

## Run in development with Docker Compose

Requirements: Docker Desktop with Docker Compose.

From the `backend` directory, copy the example environment file if you do not
already have a local `.env`, then build and start both services:

```powershell
Copy-Item .env.example .env
docker compose up --build -d
```

The API source directory is mounted into the container and Uvicorn watches
`app/`. After editing Python files, the API reloads automatically; you do not
need to start FastAPI separately or rebuild the image. You can run
`docker compose up -d` to ensure both services are started.

Rebuild only when changing dependencies in `requirements.txt` or the
`Dockerfile`:

```powershell
docker compose up --build -d
```

Check that both services are running and that the API can reach PostgreSQL:

```powershell
docker compose ps
Invoke-RestMethod http://localhost:8000/health
```

The health endpoint should return `status: ok` and `database: connected`.
Interactive API documentation is available at `http://localhost:8000/docs`.

Useful commands:

```powershell
docker compose logs -f api
docker compose logs -f db
docker compose down
```

PostgreSQL data is stored in the `postgres_data` Docker volume and is preserved
by `docker compose down`. To remove the database and all its data as well, run
`docker compose down -v`.

## Database schema

The models use PostgreSQL and PostGIS. Compose starts the PostGIS database, but
it does not create the model tables: Alembic migrations still need to be
configured and applied before using database-backed features. The `/health`
endpoint only checks that PostgreSQL is reachable.

## Run the API locally

Install the requirements in a Python virtual environment, start PostgreSQL,
set `DATABASE_URL` to a PostgreSQL connection string, then run:

```powershell
uvicorn app.main:app --reload
```
