CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    timestamp BIGINT,
    voltage REAL,
    temperature REAL
);