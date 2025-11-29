-- name: CreateMerch :one
insert into merch (name, info, image_url, points_needed)
values ($1, $2, $3, $4)
returning *;

-- name: GetMerchByID :one
select * from merch
where id = sqlc.arg(id);

-- name: GetAllMerch :many
select * from merch
ORDER BY name;

-- name: UpdateMerch :one
update merch
set
    name   = coalesce(sqlc.narg('name'), name),
    info  = coalesce(sqlc.narg('info'), info),
    image_url  = coalesce(sqlc.narg('image_url'), image_url),
    points_needed  = coalesce(sqlc.narg('points_needed'), points_needed)
where
    id = $1
returning *;

-- name: DeleteMerch :exec
delete from merch
where id = $1
returning id;
