-- name: UpsertPoints :one
INSERT INTO points (user_id, total_points)
VALUES ($1, $2)
ON CONFLICT (user_id) DO UPDATE SET
    total_points = points.total_points + EXCLUDED.total_points
RETURNING *;

-- name: GetPointsByUserID :one
SELECT * FROM points
WHERE user_id = sqlc.arg(user_id);