CONTAINER_NAME = api

build: ## Собрать images Docker
	docker compose build

start: ## Запустить контейнеры Docker
	docker compose up --build


bash: ## Открыть оболочку bash в контейнере 'api'
	docker compose exec $(CONTAINER_NAME) bash

drop: ## Остановить и удалить контейнеры Docker
	docker compose down -v


lock: ## Обновить зависимости проекта с использованием poetry
	docker compose run --build --user=root --rm $(CONTAINER_NAME) poetry lock

migrations:  ## Создать миграции
	docker compose run --build --user=root --rm $(CONTAINER_NAME) python manage.py makemigrations

test: ## Запустить pytest для тестирования проекта
	docker compose run --build --rm $(CONTAINER_NAME) pytest

