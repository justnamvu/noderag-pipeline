.PHONY: run format lint check build up down

run:
	uvicorn app.main:app --reload

# auto-format all code
format:
	black app/

# check for style issues
lint:
	flake8 app/ 

# format then lint in one shot
check: format lint

build:
	docker-compose build

# start all Docker services
up:
	docker-compose up

# stop all Docker services
down:
	docker-compose down