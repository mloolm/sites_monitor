#!/bin/sh
echo "STARTING SERVER..."
until mysqladmin ping -h "db" -u "$DB_USER" -p"$DB_PASSWORD" --silent; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready!"

# Apply migrations
alembic upgrade head

# Start server
if [ "$STAGE" = "dev" ]; then
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
  uvicorn main:app --host 0.0.0.0 --port 8000
fi