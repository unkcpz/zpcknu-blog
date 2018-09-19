+++
title = "Build postgresql by Docker for aiida using"
Description = "使用Docker搭建aiida使用所用的postgresql数据库"
Tags = ["aiida", "docker"]
Categories = ["tutorial"]
date = 2018-08-29
+++

## 目的
通过一下命令可以以`aiida`用户访问`aiidadb`数据库。
```bash
$ psql -h localhost -p 5432 -d aiidadb -U aiida
```
## 镜像

### 准备镜像文件
使得打开镜像时可以直接添加用户和数据库。
写`Dockerfile`为：
```docker
# Use an official postgres 9.6.10 image                                                                                      
FROM postgres:9.6.10

# Set the working directory to /docker-entrypoint-initdb.d
WORKDIR /docker-entrypoint-initdb.d

# Copy the current directory contents into the container at /docker-entrypoint-initdb.d
ADD postgres-conf/* /docker-entrypoint-initdb.d
```

其中`postgres-conf`文件夹下放置`init-user-db.sh`:
```bash

#!/bin/bash                                                                                                                  
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER aiida WITH PASSWORD 'aiida';
        CREATE DATABASE aiidadb OWNER aiida;
        GRANT ALL PRIVILEGES ON DATABASE aiidadb TO aiida;
EOSQL
```

### 构建镜像
在`Dockerfile`所在的文件下执行：
```bash
$ docker build -t postgres .
```
此时就有了一个构建好的`image`:
```bash
$ docker image ls

REPOSITORY            TAG                 IMAGE ID
postgres              latest              326387cea398
```

### 上传`image`
```bash
$ docker login
```

为镜像做标签，并上传到dockhub：
```bash
$ docker tag postgres unkcpz/aiida_pg:9.6.10
$ docker push unkcpz/aiida_pg:9.6.10
```

## 使用镜像

### 建立独立的共享卷
```bash
$ docker volume create aiida-db
$ docker run -it --rm -v aiida-db:/var/lib/postgresql/data unkcpz/aiida_pg:9.6.10
The files belonging to this database system will be owned by user "postgres".
...
( once it\'s finished initializing successfully and is waiting for connections, stop it )
```

新建volume后，会将创建的卷挂在到`/var/lib/docker/volumes/`中，可使用一下命令查看新建volume的
信息。
```bash
$ docker volume inspect <volume-name>
```
输出:
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

### 改变镜像中`/var/lib/postgresql/data`的所有权
这样就能用特定用户`--user`参数来运行镜像，但是使用的在使用用户`1000`也就是`$(id -u)`不在/etc/passwd中，
所以需要改变所有权：
```bash
$ docker run -it --rm -v aiida-db:/var/lib/postgresql/data bash chown -R 1000:1000 /var/lib/postgresql/data
```

### 后台运行镜像
```bash
$ docker run --rm --user 1000:1000 \
 --name aiida-postgres -v aiida-db:/var/lib/postgresql/data \
  -p 5432:5432 -d unkcpz/aiida_pg:9.6.10
```

此时可以连接数据库:
```bash
$ psql -h localhost -p 5432 -d aiidadb -U aiida
```

## 备份和重载数据库

Backup:
```bash
$ docker exec -t -u postgres aiida-postgres pg_dumpall -c > /data/db_backup/dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```

Restore:
```bashrc
cat <your_dump>.sql | docker exec -i aiida-postgres psql -U postgres
```
