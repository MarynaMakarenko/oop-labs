# Lab 2 — Backend API

Django REST Framework API with JWT authentication.

## Stack

| Concern | Technology |
|---|---|
| Framework | Django 5 + Django REST Framework |
| Auth | JWT via `djangorestframework-simplejwt` |
| ORM & Migrations | Django ORM + Django Migrations |
| Database | PostgreSQL via psycopg2 |
| CORS | django-cors-headers |

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

createdb hotel_booking_lab2
python manage.py migrate
python manage.py shell -c "
from booking.models import User
User.objects.create_user('admin', password='admin123', role='admin', full_name='Administrator')
User.objects.create_user('client1', password='pass123', role='client', full_name='John Doe')
"
python manage.py runserver 8000
```

## API Endpoints

| Method | URL | Access |
|---|---|---|
| POST | `/api/auth/token/` | Public |
| POST | `/api/auth/token/refresh/` | Public |
| POST | `/api/auth/register/` | Public |
| GET  | `/api/auth/me/` | Any auth |
| GET/POST | `/api/rooms/` | GET: any auth; POST: admin |
| GET/PUT/DELETE | `/api/rooms/<id>/` | GET: any auth; rest: admin |
| GET/POST | `/api/bookings/` | Auth (client sees own) |
| GET | `/api/bookings/<id>/` | Owner or admin |
| POST | `/api/bookings/<id>/approve/` | Admin |
| POST | `/api/bookings/<id>/reject/` | Admin |
| GET | `/api/invoices/` | Auth (client sees own) |
| POST | `/api/invoices/<id>/pay/` | Client (own) |

## Run Tests

```bash
python manage.py test booking
```
