# OOP Labs — Hotel Booking System

| Lab | Description | Stack |
|-----|-------------|-------|
| [lab1/](lab1/) | Web app with manual MVC, custom router, DAO | Python `http.server` + `psycopg2` + Jinja2 |
| [lab2/backend/](lab2/backend/) | REST API with ORM, migrations, JWT | Django + DRF + PostgreSQL |
| [lab2/frontend/](lab2/frontend/) | SPA with JWT auth, client/admin UI | React + Vite + React Router |

## Domain

**Hotel Booking System**: clients submit booking requests → admin assigns a room → system generates an invoice → client pays.

Entities: `User` (client/admin), `Room`, `Booking`, `Invoice`.
