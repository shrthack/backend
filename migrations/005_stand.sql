-- +goose Up
CREATE TABLE stand (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    info TEXT NOT NULL,
    location TEXT NOT NULL,
    image_url TEXT NOT NULL
);
