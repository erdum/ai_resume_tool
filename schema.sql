CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    whatsapp_number TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    json_data TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
