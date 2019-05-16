+++
title = "Build postgresql by Docker for aiida using"
Description = "Docker a PostgreSQL for AiiDA"
Tags = ["aiida", "docker", "postgresql"]
Categories = ["tutorial"]
date = 2018-08-29
lastmod = 2019-05-09
+++

## Target
Firstly, I wanna accessing PostgreSQL `aiidadb` with username `aiida` use following command:
```bash
$ psql -h localhost -p 5432 -d aiidadb -U aiida
```

Secondly, the database is stored in a specific directory such as `/var/lib/docker/volumes/`, distinguish from other PostgreSQL database.

### Why use Docker here?

- The database dose not affect and destroy existing PostgreSQL database in the system.
- Every aiida's virtualenvs can have their own database with username `aiida` and dbname `aiidadb`.
- Easily deploy in a new machine if you have a Docker image already. (You can use the image which is build by me.)

At this time you may ask, why not load aiida and its plugins
at the same time within a Docker image.
In my usage scenario, aiida's database interface are relatively stable, but I use different aiida version and different plugins which distributed in different python virtualenvs.

## Build and upload Docker image

### Prepare image dockerfile
In order to adding user and db in PostgreSQL, I build the following image. You can build image according to your needs.
This docker image inherit from postgres:9.6.10.

Creating and enter a directory, edit the `Dockerfile` and `postgres-conf/init-user-db.sh`.

`Dockerfile`：
```docker
# Use an official postgres 9.6.10 image                                                                                      
FROM postgres:9.6.10

# Set the working directory to /docker-entrypoint-initdb.d
WORKDIR /docker-entrypoint-initdb.d

# Copy the current directory contents into the container at /docker-entrypoint-initdb.d
ADD postgres-conf/* /docker-entrypoint-initdb.d
```

init-user-db.sh`:
```bash
#!/bin/bash                               
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER aiida WITH PASSWORD 'aiida';
        CREATE DATABASE aiidadb OWNER aiida;
        GRANT ALL PRIVILEGES ON DATABASE aiidadb TO aiida;
EOSQL
```

### Build
Execute：
```bash
$ docker build -t postgres .
```
Now you have a `image`:
```bash
$ docker image ls

REPOSITORY            TAG                 IMAGE ID
postgres              latest              326387cea398
```

### upload the image
Login to dockhub,
```bash
$ docker login
```

Tag the image，and upload it to dockhub：
```bash
$ docker tag postgres unkcpz/aiida_pg:9.6.10
$ docker push unkcpz/aiida_pg:9.6.10
```

## Using the image

### Create shared volume and link to the image
To achieve synchronization between the docker database and local storage, I create a shared volume.

```bash
$ docker volume create aiida-db
$ docker run -it --rm -v aiida-db:/var/lib/postgresql/data unkcpz/aiida_pg:9.6.10
The files belonging to this database system will be owned by user "postgres".
...
( once it\'s finished initializing successfully and is waiting for connections, stop it )
```

After creating new shared volume, it will be mounted on `/var/lib/docker/volume/`. Checking the newly created volume with:
```bash
$ docker volume inspect <volume-name>
```

Get:
```json
[
    {
        "CreatedAt": "2018-09-19T11:04:58+08:00",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/aiida-dev-db/_data",          
        "Name": "aiida-dev-db",
        "Options": {},
        "Scope": "local"
    }
]
```

### Change owenership of  `/var/lib/postgresql/data`
In order to running image with parameter `--user 1000:1000`,  
change the ownership of `/var/lib/postgresql/data` in the docker container (because user `1000` aka `$(id -u)` is not stay in /etc/passwd)：
```bash
$ docker run -it --rm -v aiida-db:/var/lib/postgresql/data bash chown -R 1000:1000 /var/lib/postgresql/data
```

### Running docker image
```bash
$ docker run --rm --user 1000:1000 \
 --name aiida-postgres -v aiida-db:/var/lib/postgresql/data \
  -p 5432:5432 -d unkcpz/aiida_pg:9.6.10
```

Accessing database with following command:
```bash
$ psql -h localhost -p 5432 -d aiidadb -U aiida
```

Or you can start and stop with the virtualenv by editing `activate` file of the virtualenv.
Add following lines in `deactivate()` function to stop docker container when deactivate the virtualenv:

```bash
{docker stop $DOCKER_DB_NAME} || {echo "Docker DB not running"}
```

Add following lines in activate parts to start docker container when activate the virtualenv.
```bash
DOCKER_DB_NAME="<docker-container-name>"
docker run --rm --user 1000:1000  --name $DOCKER_DB_NAME -v aiida-dev-db:/var/lib/postgresql/data -p 5432:5432 -d unkcpz/aiida_pg:9.6.10
echo "Start Docker DB container $DOCKER_DB_NAME"
```


## Backup and Restore the database

Backup:
```bash
$ docker exec -t -u postgres aiida-postgres pg_dumpall -c > /data/db_backup/dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```

Restore:
```bashrc
cat <your_dump>.sql | docker exec -i aiida-postgres psql -U postgres
```
