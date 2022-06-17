![Foodgram workflow](https://github.com/FinemechanicPub/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Foodgram

Поиск и публикация рецептов.

## Установка

Проект предполагает запуск в контейнере.

Внутри папки infra необходимо создать файл ".env" для настройки переменных окружения в контейнере.

- `POSTGRES_DB` - имя создаваемой базы данных
- `POSTGRES_USER` - имя пользователя базы данных
- `POSTGRES_PASSWORD` - пароль пользователя базы данных
- `DJANGO_SECRET` - настройка кода SECRET_KEY в Django
- `ALLOWED_HOSTS` - разрешенные адреса подключения к Django

Пример файла [.env](/infra/.env.sample)

```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345678
DJANGO_SECRET=2x$e%!k_u_0*gq0s4!_u(2(^lpy&gir0hg)q&5nurj0-sseuav
ALLOWED_HOSTS=127.0.0.1,10.0.0.1
```

Запустите приложение в контейнере командой

```bash
sudo docker compose up -d
```

## Настройка проекта

Создание базы данных для Djnago

```bash
sudo docker compose exec web python manage.py migrate
```

Сборка статических элементов

```bash
sudo docker compose exec web python manage.py collectstatic
```

Создание администратора Django

```bash
sudo docker compose exec web python manage.py createsuperuser
```

Заполнение базы данных тестовыми записями

```bash
sudo docker compose exec web python manage.py sampledata
```

## Документация

После запуска приложения документация API доступна по адресу [http://127.0.0.1/redoc/](http://127.0.0.1/redoc/)

## Технологии

Приложение работает на
- [Django 2.2](https://www.djangoproject.com/download/)
- [Django REST Framework 3.12](https://www.django-rest-framework.org/#installation).
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).
- [PostgreSQL 13.0](https://www.postgresql.org/).


## Разработчики

Проект разработан 
- [Александр Рубцов](https://github.com/FinemechanicPub)
- [Анастасия Дементьева](https://github.com/Nastasia153)
- [Виталий Насретдинов](https://github.com/nasretdinovs)

## Демонстрация
![Website](https://img.shields.io/website?down_color=lightgrey&down_message=%D0%BD%D0%B5%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82&label=%D1%81%D0%B0%D0%B9%D1%82&up_color=blue&up_message=%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82&url=http%3A%2F%2Ffinemechanic.hopto.org%2Fredoc%2F)

[http://finemechanic.hopto.org/redoc/](http://finemechanic.hopto.org/redoc/)