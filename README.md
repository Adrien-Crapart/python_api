## Run all development files

For windows environment use that
`cd api`
`.venv\Scripts\activate.ps1`
`python app.py / flask run`
`pip install -r requirements.txt`

## Build docker image

docker ps
docker run --name=nginx -d -p 80:80 nginx
docker inspect <container ID>
docker inspect <container id> | findstr "IPAddress"
docker volume create pg_data
docker run --name=postgis -d -e POSTGRES_USER=alex -e POSTGRES_PASS=password -e POSTGRES_DBNAME=gis -e ALLOW_IP_RANGE=0.0.0.0/0 -p 5432:5432 -v pg_data:/var/lib/postgresql --restart=always kartoza/postgis:9.6-2.4
docker logs postgis

`docker build -t rest-apis-flask .`
`docker run -dp 5005:5000 rest-apis-flask`
`docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-apis-flask`
docker-compose up / docker-compose up -d --build
`docker-compose down -v`
docker network create tulip-net
docker network connect tulip-net flask-api

## Aiflow running tasks

`docker exec -it  api-airflow-scheduler-1 /bin/bash`
airflow tasks test user_processing extract_user 2023-01-28
docker cp api-airflow-scheduler-1:/opt/airflow/airflow.cfg .

`docker ps`
`docker exec -it postgresql_db bash`
`find / -name pg_hba.conf`
`docker cp postgresql_db:/var/lib/postgresql/data/pg_hba.conf .`
`docker cp pg_hba.conf postgresql_db:/var/lib/postgresql/data/pg_hba.conf`

## Run migrations

`flask db init`
`flask db migrate`
`flask db upgrade`

## Git usage

`git init`
`git add myfile.py` OR `git add .`
`git rm --cached scheamas.py`
`git checkout -- app.py`
`git restore app.py`
`git commit -m "message"`
`git branch -M main`
`git remote add origin https://github.com/Adrien-Crapart/data-api.git`
`git push` OR `git push -u origin main`
`git reset COMMIT_ID`
`git revert COMMIT_ID`
