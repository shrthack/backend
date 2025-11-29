-- name: CreateAnalytics :one
INSERT INTO analytics (user_id, stand_id) VALUES ($1, $2) RETURNING *;

-- name: GetAnalyticsGrouped :many
SELECT DATE(time) as date, EXTRACT(hour from time) as hour, COUNT(*) as count
FROM analytics
GROUP BY DATE(time), EXTRACT(hour from time)
ORDER BY DATE(time), EXTRACT(hour from time);