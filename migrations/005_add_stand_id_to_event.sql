-- +goose Up
ALTER TABLE event ADD COLUMN stand_id uuid REFERENCES stand(id);