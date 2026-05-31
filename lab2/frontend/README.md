# Lab 2 — Frontend

React SPA with JWT authentication, communicates with the Django backend API.

## Stack

| Concern | Technology |
|---|---|
| Framework | React 18 + Vite |
| Routing | React Router v6 |
| HTTP client | Axios (with JWT interceptors) |
| Auth | JWT stored in localStorage, auto-refresh |
| Styling | Bootstrap 5 (CDN) |
| Tests | Vitest + React Testing Library |

## Setup

```bash
npm install
npm run dev
```

Open http://localhost:5173 (requires backend running on port 8000).

## Features

- Login / logout with JWT
- **Client**: create booking requests, view bookings & invoices, pay invoices
- **Admin**: view all bookings, assign rooms, approve/reject, manage room CRUD
- Protected routes redirect unauthenticated users to `/login`

## Run Tests

```bash
npm test
```
