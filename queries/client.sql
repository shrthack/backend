-- name: CreateClient :one
insert into client (email, password_hash, name, surname, image_url, tg_username)
values ($1, $2, $3, $4, $5, $6)
returning *;

-- name: GetClientByID :one
select * from client
where id = sqlc.arg(id);

-- name: GetClientByEmail :one
select * from client
where email = sqlc.arg(email);

-- name: UpdateClient :one
update client
set
    name   = coalesce(sqlc.narg('name'), name),
    surname  = coalesce(sqlc.narg('surname'), surname),
    image_url  = coalesce(sqlc.narg('image_url'), image_url),
    tg_username  = coalesce(sqlc.narg('tg_username'), tg_username)
where
    id = $1
returning *;

-- name: DeleteClient :exec
delete from client
where id = $1
returning id;
