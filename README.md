![Foodgram workflow](https://github.com/FinemechanicPub/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Foodgram

Поиск и публикация рецептов.

## Компиляция кода Frontend и запуск в режиме отладки

Этот способ используется, если требуется изменять код Frontend или Backend.

Перейдите в папку `deployment_dev` и выполните команду 

```bash
sudo docker compose up -d
```

Будет произведена сборка кода Frontend и запуск сервера Nginx, настроенного на работу с отладочным сервером Django.

Перейдите в папку `backend` и выполните команды:

Создание и активация окружения
```bash
python -m venv venv
source venv/bin/activate
```
Установка зависимостей
```bash
pip install -r requirements.txt
```

Создание базы данных для Djnago

```bash
python foodgram/manage.py migrate
```

Создание администратора Django

```bash
python foodgram/manage.py createsuperuser
```

Заполнение базы данных тестовыми записями (ингредиенты и теги)

```bash
python foodgram/manage.py sample_data
```

Для запуска сервера в отладочном режиме установите переменну среды `DJANGO_DEBUG`.

Сервер запускается командой

```bash
python foodgram/manage.py runserver
```

## Установка в рабочем режиме

Проект предполагает запуск в контейнере, на основе загружаемого из Интернет образа.

Внутри папки deployment необходимо создать файл ".env" для настройки переменных окружения в контейнере.

- `DB_ENGINE` - система управления базами данных
- `POSTGRES_DB` - имя создаваемой базы данных
- `POSTGRES_USER` - имя пользователя базы данных
- `POSTGRES_PASSWORD` - пароль пользователя базы данных
- `DJANGO_SECRET` - настройка кода SECRET_KEY в Django
- `ALLOWED_HOSTS` - разрешенные адреса подключения к Django

Пример файла [.env](/deployment/.env.sample)

```
DB_ENGINE=django.db.backends.postgresql
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

## Настройка проекта в рабочем режиме

Создание базы данных для Django

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

Заполнение базы данных тестовыми записями (ингредиенты и теги)

```bash
sudo docker compose exec web python manage.py sample_data
```

## Документация

После запуска приложения документация API доступна по адресу [http://127.0.0.1/api/docs/](http://127.0.0.1/api/docs/)

## Технологии

Приложение работает на
- [Django 2.2](https://www.djangoproject.com/download/)
- [Django REST Framework 3.12](https://www.django-rest-framework.org/#installation).
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).
- [PostgreSQL 13.0](https://www.postgresql.org/).


## Разработчики

Проект разработан 
- [Александр Рубцов](https://github.com/FinemechanicPub)

## Демонстрация
![Website](https://img.shields.io/website?down_color=lightgrey&down_message=%D0%BD%D0%B5%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82&label=%D1%81%D0%B0%D0%B9%D1%82&up_color=blue&up_message=%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82&url=http%3A%2F%2Ffinemechanic.hopto.org%2Fredoc%2F)

[http://finemechanic.hopto.org/](http://finemechanic.hopto.org/)

[http://finemechanic.hopto.org/api/docs/](http://finemechanic.hopto.org/api/docs/)