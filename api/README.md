# `/api`

This folder contains a **FastAPI-based API** for accessing analytical insights from the Medical Telegram Warehouse. It exposes endpoints to query messages, channel activity, product mentions, and visual content statistics from the cleaned database schema.

---

## API Overview

The API provides the following endpoints:

1. **Top Products** – `/api/reports/top-products`

   * Returns the most frequently mentioned products/terms.

2. **Channel Activity** – `/api/channels/{channel_name}/activity`

   * Returns daily message counts for a specific Telegram channel.

3. **Search Messages** – `/api/search/messages`

   * Searches for messages containing a given keyword.

4. **Visual Content Stats** – `/api/reports/visual-content`

   * Returns statistics about images (e.g., YOLO-detected categories) across channels.

---

## Files

* `schemas.py` – Pydantic models defining API response schemas.
* `main.py` – Database connection setup and session dependency.
* `database.py` – Contains the SQLAlchemy `SessionLocal`, `engine`, and `Base`.
* `routes/` *(optional, if routes are separated)* – Could include endpoint definitions.

---

## Environment Setup

1. **Install dependencies**

```bash
pip install fastapi uvicorn python-dotenv sqlalchemy psycopg2-binary
```

2. **Create a `.env` file** in the project root with database credentials:

```
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=medical_db
```

---

## Running the API

Start the FastAPI server locally on port 8000:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

* Access the API at [http://localhost:8000](http://localhost:8000)
* Interactive API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Notes

* Ensure the PostgreSQL database is running and populated with the `clean` schema.
* The API relies on SQLAlchemy sessions for database access (`get_db()` dependency).
* Queries are optimized for the cleaned tables produced by the ETL pipeline.


