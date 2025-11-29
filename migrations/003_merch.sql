-- +goose Up
CREATE TABLE merch (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    info TEXT NOT NULL,
    image_url TEXT NOT NULL,
    points_needed INT NOT NULL,
);
