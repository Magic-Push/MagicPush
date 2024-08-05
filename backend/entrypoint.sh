#!/bin/sh

# Navigate to the application directory
cd magicpush

# Set environment variables
export DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
export FLASK_APP=__init__.py

# Run database migrations
rm -r -f migrations
flask db init
flask db migrate
flask db upgrade

cd ..

# Start Gunicorn
exec gunicorn -c gunicorn.conf.py -b 0.0.0.0:6969 gunicorn_app:app