-- +goose Up
CREATE TABLE points (
    user_id uuid PRIMARY KEY REFERENCES client(id),
    total_points INT NOT NULL
);
