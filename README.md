# Foodgram

## Проект "Продуктовый помощник"

[![Foodgram workflow](https://github.com/tanja-ovc/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/tanja-ovc/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

**Foodgram** - платформа для обмена рецептами.

Здесь пользователи смогут 
- публиковать рецепты,
- подписываться на публикации других пользователей,
- добавлять понравившиеся рецепты в список «Избранное»,
- перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Этот проект содержит код фронтенда, бэкенда и инфраструктуры для локальной разработки в Docker-контейнерах.Авторство кода фронтенда принадлежит Яндекс.Практикуму.

Проект также ранее размещался на удалённом сервере на Яндекс.Облаке.

_Примечание:_ на данный момент удалённый сервер, где я размещала проект, не работает в связи с истечением гранта на использование виртуальной машины на Яндекс.Облаке.

### Технологии

Python3.7, Django REST Framework, Docker, nginx, Gunicorn, GitHub Actions

### Инфраструктура

Проект содержит в себе всё необходимое для для локальной разработки в Docker-контейнерах.

Принцип разворачивания проекта с помощью Docker-контейнеров описан мной в README предыдущих проектов здесь:

- локальный деплой: https://github.com/tanja-ovc/docker_local_containers#docker-yamdb-local

- деплой на удалённом сервере: https://github.com/tanja-ovc/docker_remote_containers#docker-yamdb-remote

### Установка

Клонировать репозиторий и перейти в него в командной строке:

```https://github.com/tanja-ovc/docker_local_containers.git```

Убедиться, что находитесь в директории _docker_local_containers/_, либо перейти в неё:

```cd docker_local_containers/```

Cоздать виртуальное окружение:

```python3 -m venv venv```

Активировать виртуальное окружение:

* Для Mac:
 
    ```source venv/bin/activate```

* Для Windows:

    ```source venv/Scripts/activate```

При необходимости обновить pip:

```pip install --upgrade pip```

### Запуск проекта локально

Для запуска контейнеров необходим установленный Docker.

Перейдите в директорию _infra/_, где находится файл docker-compose. Соберите контейнеры:

```docker-compose up```

Выполните по очереди команды (выполнить миграции, создать суперпользователя и собрать статику):

```docker-compose exec backend python manage.py migrate```

```docker-compose exec backend python manage.py createsuperuser```

```docker-compose exec backend python manage.py collectstatic --no-input```

Теперь проект доступен локально.
________________________________

Примеры адресов, по которым можно обратиться, чтобы проверить корректную работу проекта:

http://localhost/signup - страница регистрации,

http://localhost/recipes - главная страница,

http://localhost/admin/ - админка,

http://localhost/api/docs/redoc.html - документация API Foodgram.

### Заполнение БД ингредиентами

Заполнение таблицы ингредиентов в БД прилагающимися данными в формате .csv можно произвести с помощью команды

```sudo docker-compose exec backend python manage.py import_data```

### Авторство

Код management-команды для загрузки данных из .csv файла в БД написал мой бывший соратник по команде Василий Кузьминых (я только изменила команду под текущие нужды).

Всё остальное написала я, Татьяна Овчинникова.

_Время написания: февраль-март 2022 г_
