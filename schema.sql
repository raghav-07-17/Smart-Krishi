PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS farm_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop TEXT NOT NULL DEFAULT 'paddy',
    area_acres REAL NOT NULL CHECK (area_acres > 0),
    field_type TEXT NOT NULL,
    growth_stage TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diagnosis_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    symptoms TEXT NOT NULL,
    photo_path TEXT,
    possible_result TEXT,
    review_status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farm_records(id)
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    pack_size REAL,
    pack_unit TEXT,
    price_inr REAL,
    price_checked_at TEXT,
    verification_status TEXT NOT NULL DEFAULT 'unverified'
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop TEXT NOT NULL,
    condition_name TEXT NOT NULL,
    advice TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_url TEXT,
    reviewed_by TEXT,
    reviewed_at TEXT,
    status TEXT NOT NULL DEFAULT 'pending_review'
);