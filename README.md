# О проекте

Телеграм-бот для помощи инженерам в работе.

Функционал бота:
* предоставлять акты, инструкции и полезные файлы.
* связь с сотрудником технической поддержки.
* меню администратора

# Requirements

* Python 3.10
* Docker 20.10+ [(инструкция по установке)](https://docs.docker.com/get-docker/).

# Клонирование репозитория
Склонируйте репозиторий git clone git@github.com:SergoSolo/servcontrol_bot.git

# Запуск проекта

Все команды выполняются из корневой директории проекта.

<details>
<summary>Проверка docker</summary>
<br>
По умолчанию проект запускается в докере. Для начала нужно убедиться, что докер
установлен. Открой любой терминал и выполни следующую команду:

```shell
docker --version
```
Должна быть выведена версия докера, это выглядит примерно так:
```
Docker version 20.10.21, build baeda1f
```
Если докер не установлен, то установите его, следуя [инструкции](https://docs.docker.com/get-docker/).
</details>

<details>
<summary>Настройка переменных окружения</summary>
<br>

Переменные окружения проекта хранятся в файле `.env` , для которого есть шаблон `.env.template`.
Создай в корне проекта файл `.env` простым копированием файла `.env.template`.

</details>

<details>
<summary>Запуск сервисов</summary>
<br>
<hr>

Для запуска проекта выполни следующую команду:
```
docker-compose up -d --build
```

Убедимся, что все контейнеры запущены:
```
docker-compose ps
```

Результат должен быть примерно такой (список сервисов может отличаться, но статус всех сервисов
должен быть `running`):
```
NAME                COMMAND                  SERVICE             STATUS              PORTS
serv_bot            "sh -c 'alembic upgr…"   bot                 running
serv_db             "docker-entrypoint.s…"   db                  running             0.0.0.0:5432->5432/tcp
```

Чтобы заработал бот, нужно задать действующий токен бота для переменной `BOT_TOKEN` в файле `.env`,
а затем снова запустить все сервисы через `docker-compose`.

Остановить и удалить запущенные контейнеры:
```
docker-compose down
```
</details>

##  Используемые технологии:
- Python version 3.10
- Aiogram
- Alembic
- SQLAlchemy
- Pydantic


## Автор:
> [Sergey](https://github.com/SergoSolo)