# Dockerized Claims App

This stack starts a PostgreSQL database and a small Python API. On app startup, it initializes PostgreSQL, creates the `claims` and `citations` tables if needed, and loads source rows from the configured claims TSV/CSV inputs and citations CSV file.
The stack now defaults to a pgvector-enabled PostgreSQL image so patent embeddings can be stored natively as vectors.

The full-data preset reads claims from `data/claims/` and citations from `data/citations.csv`. Smaller sample files are also bundled:

- `data/claims/g_claims_2013.tsv`
- `data/samples/claims.tsv`
- `data/samples/claims_8549171.tsv`
- `data/samples/citations.csv`

Claims imports can now come from one file or several files. The app reads:

- `CLAIMS_PATHS`: a `:`-separated list of files, directories, or glob patterns
- `CLAIMS_PATH`: the single-file fallback when `CLAIMS_PATHS` is empty
- `CITATIONS_PATH`: the citations CSV path

Example multi-file configuration in `.env`:

```bash
CLAIMS_PATHS=/opt/app/data/claims
CITATIONS_PATH=/opt/app/data/citations.csv
```

## What gets created

- PostgreSQL database: `patents`
- Tables:
  - `claims`
  - `citations`
  - `patent_embeddings`

The seed process is idempotent. Re-running the stack updates existing claims by `(patent_id, claim_number)` and citations by `(app_id, parsed)`.
The same seed process can also be triggered again after startup with `POST /initialize`.

## Claims Schema

Each row in `claims` contains:

- `patent_id`
- `claim_sequence`
- `claim_text`
- `dependent`
- `claim_number`
- `exemplary`
- `created_at`

Each row in `citations` contains:

- `app_id`
- `citation_pat_pgpub_id`
- `parsed`
- `form892`
- `form1449`
- `citation_in_oa`
- `created_at`

Each row in `patent_embeddings` contains:

- `embedding_name`
- `patent_id`
- `embedding`

The default patent embedding model is `sentence-transformers/all-MiniLM-L6-v2`, which produces 384-dimensional vectors, so `patent_embeddings.embedding` is created as `vector(384)`.

At the end of a successful run, the container logs the list of claims files it is loading and a summary like:

```text
Database initialized with <claims> claims across <patents> patents and <citations> citations.
```

The expected boot order is:

1. `Initializing database and loading claims and citations data...`
2. `Database initialized with ...`

## Run

Two presets are included:

- `sample`: fast startup with `data/samples/claims_8549171.tsv` and `data/samples/citations.csv`
- `full`: full startup with `data/claims/` and `data/citations.csv`

Each preset uses a different PostgreSQL volume and host ports, so they can be run independently without reusing the same database state.

From the `docker/` directory:

```bash
cp .env.example .env
docker compose up --build
```

That legacy flow is now equivalent to a customizable full-data setup. For the two standard presets, use either `make` or `docker compose --env-file`.

### Sample dataset

```bash
make up-sample
```

Equivalent command:

```bash
docker compose --env-file .env.sample -p claims-sample up --build
```

Services:

- API: `http://localhost:8001`
- PostgreSQL: `localhost:5434`

### Full dataset

```bash
make up-full
```

Equivalent command:

```bash
docker compose --env-file .env.full -p claims-full up --build
```

The services will be available at:

- API: `http://localhost:8000`
- PostgreSQL: `localhost:5433`

If you already run PostgreSQL locally on `5432`, keep the container on `5433` or change `POSTGRES_PORT` in `.env` to any free host port.

The stack defaults to `pgvector/pgvector:pg15` so the database can store embedding vectors natively. If you want PostgreSQL 16 instead, set `POSTGRES_IMAGE=pgvector/pgvector:pg16` and recreate the volume.

The preset env files also use explicit volume names so the sample and full databases stay isolated from each other.

The full-data import is large enough to trigger PostgreSQL checkpoint hints with the default WAL limit, so the full preset uses `POSTGRES_MAX_WAL_SIZE=4GB` by default. Raise or lower that value in the selected env file if your machine needs a different tradeoff between WAL disk usage and checkpoint frequency.

To stop a preset:

```bash
make down-sample
make down-full
```

## Useful endpoints

- `GET /health`
- `GET /stats`
- `POST /initialize`
- `GET /claims?limit=20`
- `GET /claims/<patent_id>`
- `GET /citations?limit=20`
- `GET /citations/<app_id>`

Example:

```bash
curl http://localhost:8000/stats
curl -X POST http://localhost:8000/initialize
curl http://localhost:8000/claims?limit=5
curl http://localhost:8000/claims/8549171
curl http://localhost:8000/citations?limit=5
curl http://localhost:8000/citations/12000001
```

`POST /initialize` re-runs the same import used at container startup and returns `409` if another initialization is already in progress.

## Reset the database

To remove the persisted PostgreSQL volume and reseed from scratch:

```bash
docker compose down -v
docker compose up --build
```

This reset is also required when switching PostgreSQL major versions, for example from 15 to 16.

If you hit errors like `role "postgres" does not exist`, the old volume was initialized with different credentials. Either keep the new default volume name or set a new `POSTGRES_VOLUME_NAME` in `.env`.
# RAG-docker
