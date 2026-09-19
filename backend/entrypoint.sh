#!/bin/sh
set -e

PORT="${PORT:-9200}"

echo "Waiting for MySQL..."
python - <<'PY'
import os, time
from sqlalchemy import create_engine, text
from app.config import settings

url = settings.database_url
for i in range(60):
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database is ready.")
        break
    except Exception as e:
        print(f"DB not ready ({i+1}/60): {e}")
        time.sleep(2)
else:
    raise SystemExit("Database not ready after retries")
PY

echo "Creating tables..."
python -c "from app.database import Base, engine; from app import models; Base.metadata.create_all(bind=engine)"

if [ "${SEED_ON_START}" = "true" ] || [ "${SEED_ON_START}" = "1" ]; then
  echo "Seeding data..."
  python -c "from app.seed import seed; seed()"
fi

echo "Starting gunicorn on :${PORT}..."
exec gunicorn wsgi:app --bind "0.0.0.0:${PORT}" --workers 2 --threads 4 --timeout 120
