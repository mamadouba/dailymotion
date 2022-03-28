SHELL := /bin/bash

initdb:
	poetry run dailymotion/scripts/db.py 

runserver:
	poetry run uvicorn --host 0.0.0.0 --port 8000 dailymotion.main:app

test:
	poetry run pytest tests

black:
	poetry run black .

createdb:
	docker run --name dailymotiondb -p 5434:5432 \
	-e POSTGRES_USER=test \
	-e POSTGRES_PASSWORD=test \
	-e POSTGRES_DB=test -d postgres:latest

redis: 
	docker run -d --name redis -p 6379:6379 redis:latest
smtp:
	docker run -d --name smtp -p 1025:1025 -p 8025:8025 mailhog/mailhog
build:
	docker build . -t dailymotion 

run:
	docker run -d --name dailymotion -p 8000:8000 dailymotion 

clean:
	docker stop $(docker ps -qa)
	docker rm $(docker ps -qa)
