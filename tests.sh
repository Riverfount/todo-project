#!/usr/bin/env bash

# Start environment with docker-compose
TODO_DB=todo_test docker-compose up -d

# Wait 5 secs
sleep 5

# Ensure database is clean
docker-compose exec api todo reset-db -f
docker-compose exec api alembic stamp base

# Run migrations
docker-compose exec alembic upgrade head

# Run tests
docker-compose exec api pytest -v -l --tb=short --maxfail=1 --disable-warnings tests/

# Stop environment
docker-compose down
