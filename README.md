# YaMDb


## Описание проекта

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles), а также комментарии (Comment) на сами отзывы. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором. В каждой категории есть произведения: книги, фильмы или музыка. Каждому произведению может быть присвоен свой жанр (Genre). Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. 

В данном репозитории представлен API данного сервиса, документацию которого можно просмотреть по ссылке *http://127.0.0.1:8000/redoc/*, а также докер файлы для создания контейнеров.

пример запроса и ответа API

*http://127.0.0.1:8000/api/v1/titles/ метод GET*

```json
{
    "count": 34,
    "next": "http://127.0.0.1:8000/api/v1/titles/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Побег из Шоушенка",
            "year": 1994,
            "category": {
                "name": "Фильм",
                "slug": "movie"
            },
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "rating": 7,
            "description": ""
        },
        ...
    ]
}
```


____
## Переменные окружения .env

Проект работает с базой данных Postgres, для подключения к которой необходимы данные.
Чтобы передать их в докер контейнер проекта необходимо создать файл .env по следующему шаблону

```yaml
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```


____
## Запуск приложения в контейнерах Docker

- Склонируйте папку проекта на ваш компьютер

``` git clone https://github.com/HaRumiCoder/infra_sp2.git ```

- Перейдите в папку с файлом docker-compose.yaml

``` cd infra/ ```

- Создайте контейнеры (web, db, nginx)

``` docker-compose up ```

- В контейнере web сделайте миграции, создайте суперюзера django и соберите статику в папку api_yamdb/static/

``` docker-compose exec web python manage.py migrate ```

``` docker-compose exec web python manage.py createsuperuser ```

> в готовой фикстуре уже имеется супер юзер с данными

> login: admin25
> password: qwerty1

``` docker-compose exec web python manage.py collectstatic --no-input ```

- Далее проект будет доступен по адресу *http://localhost/*


____
## Заполнение базы данными

В репозитории имеется готовая фикстура с несколькими записями. Загрузить ее можно с помощью команды

``` docker-compose exec web python manage.py loaddata fixtures.json ```
