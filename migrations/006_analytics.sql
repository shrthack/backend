-- +goose Up
CREATE TABLE analytics (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid REFERENCES client(id),
    stand_id uuid REFERENCES stand(id),
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);