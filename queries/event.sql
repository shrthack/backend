-- name: CreateEvent :one
insert into event (name, info, image_url, points)
values ($1, $2, $3, $4)
returning *;

-- name: GetEventByID :one
select * from event
where id = sqlc.arg(id);

-- name: GetAllEvents :many
select * from event;

-- name: UpdateEvent :one
update event
set
    name = coalesce(sqlc.narg('name'), name),
    info = coalesce(sqlc.narg('info'), info),
    image_url = coalesce(sqlc.narg('image_url'), image_url),
    points = coalesce(sqlc.narg('points'), points)
where
    id = $1
returning *;

-- name: DeleteEvent :exec
delete from event
where id = $1
returning id;
