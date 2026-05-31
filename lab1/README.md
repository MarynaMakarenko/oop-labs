# Lab 1 — Hotel Booking System

Server-side web application built with Python's standard library (`http.server`, `http.cookies`) and minimal dependencies (`psycopg2`, `Jinja2`).

## Architecture

| Layer | Implementation |
|---|---|
| HTTP server / Front Controller | `http.server.BaseHTTPRequestHandler` |
| Router | Custom regex-based router (`app/core/router.py`) |
| MVC | Manual — controllers in `app/controllers/`, Jinja2 views, dataclass models |
| Data access | DAO pattern with raw SQL via `psycopg2` |
| Sessions | In-memory store + `http.cookies` |
| Logging | `logging` module, writes to `hotel.log` |

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create PostgreSQL database and run migration
createdb hotel_booking
psql hotel_booking < migrations/001_init.sql

# 4. Set environment variables (optional — defaults shown)
export DB_HOST=localhost DB_PORT=5432 DB_NAME=hotel_booking
export DB_USER=postgres DB_PASSWORD=password
export SERVER_PORT=8080

# 5. Run
python main.py
```

Open http://localhost:8080/login

Default accounts:
- **admin / admin** — administrator role
- **client1 / pass** — client role

## Run Tests

```bash
python -m pytest tests/ -v
```

## Domain Flow

1. Client submits a **Booking** request (class, guests, dates).
2. Admin reviews pending bookings, selects a suitable **Room**, approves.
3. System automatically generates an **Invoice** (nights × price/night).
4. Client pays the invoice from the invoices page.
