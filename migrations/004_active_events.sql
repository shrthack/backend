-- +goose Up
CREATE TABLE active_events (
    user_id uuid PRIMARY KEY NOT NULL,
    event_id uuid NOT NULL,
    total_points INT NOT NULL
);
