-- name: CreateStand :one
insert into stand (name, info, location, image_url)
values ($1, $2, $3, $4)
returning *;

-- name: GetStandByID :one
select * from stand
where id = sqlc.arg(id);

-- name: GetAllStands :many
select * from stand;

-- name: UpdateStand :one
update stand
set
    name = coalesce(sqlc.narg('name'), name),
    info = coalesce(sqlc.narg('info'), info),
    location = coalesce(sqlc.narg('location'), location),
    image_url = coalesce(sqlc.narg('image_url'), image_url)
where
    id = $1
returning *;

-- name: DeleteStand :exec
delete from stand
where id = $1
returning id;
