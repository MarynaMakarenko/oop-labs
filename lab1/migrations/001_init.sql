-- Hotel Booking System — initial schema

CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(64)  NOT NULL,
    role          VARCHAR(20)  NOT NULL DEFAULT 'client',
    full_name     VARCHAR(200) NOT NULL DEFAULT '',
    email         VARCHAR(200) NOT NULL DEFAULT '',
    created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rooms (
    id              SERIAL PRIMARY KEY,
    number          VARCHAR(20)    UNIQUE NOT NULL,
    capacity        INTEGER        NOT NULL,
    apartment_class VARCHAR(20)    NOT NULL,
    price_per_day   DECIMAL(10, 2) NOT NULL,
    is_available    BOOLEAN        DEFAULT TRUE,
    description     TEXT           DEFAULT '',
    created_at      TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
    id              SERIAL PRIMARY KEY,
    client_id       INTEGER     NOT NULL REFERENCES users(id),
    room_id         INTEGER              REFERENCES rooms(id),
    guests_count    INTEGER     NOT NULL,
    apartment_class VARCHAR(20) NOT NULL,
    check_in        DATE        NOT NULL,
    check_out       DATE        NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    notes           TEXT                 DEFAULT '',
    created_at      TIMESTAMP            DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoices (
    id         SERIAL PRIMARY KEY,
    booking_id INTEGER        NOT NULL REFERENCES bookings(id),
    amount     DECIMAL(10, 2) NOT NULL,
    status     VARCHAR(20)    NOT NULL DEFAULT 'unpaid',
    issued_at  TIMESTAMP               DEFAULT CURRENT_TIMESTAMP,
    paid_at    TIMESTAMP
);

-- Seed accounts
-- admin  / admin
-- client1 / pass
INSERT INTO users (username, password_hash, role, full_name, email) VALUES
    ('admin',   '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin',  'Administrator', 'admin@hotel.com'),
    ('client1', 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1', 'client', 'John Doe',      'john@example.com')
ON CONFLICT (username) DO NOTHING;

-- Seed rooms
INSERT INTO rooms (number, capacity, apartment_class, price_per_day, description) VALUES
    ('101', 2, 'economy',  60.00,  'Cosy room with city view'),
    ('102', 2, 'economy',  65.00,  'Quiet room with garden view'),
    ('201', 2, 'standard', 100.00, 'Spacious standard room'),
    ('202', 3, 'standard', 120.00, 'Standard room with extra bed'),
    ('301', 2, 'luxury',   200.00, 'Luxury suite with sea view'),
    ('302', 4, 'luxury',   280.00, 'Presidential suite')
ON CONFLICT (number) DO NOTHING;
