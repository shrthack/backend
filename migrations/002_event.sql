-- +goose Up
CREATE TABLE event (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    info TEXT NOT NULL,
    image_url TEXT NOT NULL,
    points INT NOT NULL,
);
