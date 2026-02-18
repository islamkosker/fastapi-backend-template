#!/usr/bin/env bash

set -e
set -x

# Let the DB start
python /backend/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /backend/app/seed/seeder.py

# Start FastAPI server with workers
if [[ "$ENV_FILE" != *".env.test" ]]; then
  exec fastapi run app/main.py --host 0.0.0.0 --port 80 --workers 4 --reload
fi