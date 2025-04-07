# In Code We Trust

A Flask application with SQLAlchemy and PostgreSQL.

## Setup

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Create a PostgreSQL database named `in_code_we_trust`

4. Update the `.env` file with your database credentials if needed

5. Initialize the database:
```bash
poetry run alembic upgrade head
```

## Running the Application

To run the application:
```bash
poetry run python run.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- `GET /ping` - Returns a pong response

## Database Migrations

To create a new migration:
```bash
poetry run alembic revision --autogenerate -m "description of changes"
```

To apply migrations:
```bash
poetry run alembic upgrade head
``` 
