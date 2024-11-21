# API Задач
Небольшой проект для тренировки навыков построения API на Django с нуля. 
C последующим покрытием тестами и CI/CD посредством github action.

## Как запустить проект 
- Для запуска требуется установленный docker compose

## Development версия
- Клонировать репозиторий 
```bash 
git clone https://github.com/DenisMaslennikov/to-do-list-Django.git
```
- Настроить переменные окружения в папке **config** в файле **.env** используя в качестве шаблона файл **.env.template** в той же папке.
- Запустить контейнеры. 
```bash 
docker compose up --build
```
- После запуска всех контейнеров документация Swagger будет доступна по ссылке http://127.0.0.1:8000/api/v1/schema/swagger-ui/

## Запуск тестов
- Клонировать репозиторий 
```bash 
git clone https://github.com/DenisMaslennikov/to-do-list-Django.git
```
- Настроить переменные окружения в папке **config** в файле **.env** используя в качестве шаблона файл **.env.template** в той же папке.
```bash
docker compose run --build --rm api pytest
```

