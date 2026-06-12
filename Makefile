.PHONY: run format lint check build up down

run:
	uvicorn app.main:app --reload

format: # auto-format all code
	black app/

lint: # check for style issues
	flake8 app/ 

check: format lint # format then lint in one shot

build:
	docker-compose build

up: # start all Docker services
	docker-compose up

down: # stop all Docker services
	docker-compose down