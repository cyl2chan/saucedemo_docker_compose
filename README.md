# Docker Compose Demo — Multi-Container QE Infrastructure

## What This Is
A complete working example of 3 Docker containers working together:
- **db** — PostgreSQL database (seeded with test data)
- **api** — Flask mock API server (CRUD for products)
- **test-runner** — pytest suite that validates the API

## Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop/)

## Run Everything (One Command)
```bash
docker compose up --build --abort-on-container-exit
```

## View the Test Report
After tests finish, open: `reports/report.html`

## Useful Commands
```bash
# Run tests only (after first build)
docker compose up test-runner

# Rebuild everything from scratch
docker compose build --no-cache

# Tear down everything
docker compose down -v

# Check what's running
docker compose ps

# See logs from a specific container
docker compose logs api
docker compose logs db
```

## Architecture
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   db         │     │   api        │     │  test-runner  │
│  PostgreSQL  │◄────│  Flask API   │◄────│   pytest      │
│  Port 5432   │     │  Port 5000   │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
     Container 1          Container 2          Container 3
```
