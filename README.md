# news_parser

news_parser - это новостной парсер.
Парсер оперирует 2-мя таблицами в базе данных. В таблицу "resource" добавляются ресурсы, с которых требуется спарсить новости.
В таблицу 'items' добавляется информация о найденных новостях.

Пока что парсер позволяет вытаскивать данные только по тем новостям, где для вытаскивания данных достаточно нацелиться на один единственный тэг.

В следующей версии парсера можно будет вытаскивать данные, где для доступа к данным вначале нужно вытащить один тэг с одними параметрами, потом второй с другими параметрами и т.д.

## Системные требования
- Python 3.10+
- Works on Linux, Windows, macOS

## Технологии:
- Python 3.10
- BeautifulSoup4
- PostgreSQL
- SQLAlchemy 1.4

## Как запустить проект:

Для запуска проекта на локальной машине в проект вложен docker-compose. После запуска docker-compose сайт будет доступен по адресу: http://127.0.0.1/

Необходимо выполнить следующие шаги:
- Проверить, что свободен порт 5432 (требуется для работы  Postgres)

- Проверить, что на машине установлены docker и docker-compose 

- Клонировать репозиторий и перейти в папку проекта, где расположен файл docker-compose:
```
git clone https://github.com/KostKH/private_blog.git
cd news_parser/infra_parser_dev/
```

- Cоздать в папке infra_parser_dev файл .env с переменными окружения:
```
touch .env
```
- Заполнить .env файл переменными окружения. Пример:
```
echo DB_NAME=postgres >>.env
echo POSTGRES_USER=postgres >>.env
echo POSTGRES_PASSWORD=postrgres >>.env
echo DB_HOST=db_parser >>.env
echo DB_PORT=5432 >>.env
echo LOGFILE=logfile.log >> .env
```
- Установить и запустить приложения в контейнерах:
```
docker-compose up -d
```
- Зайти в контейнер с парсером, запустить терминал bash:
```
docker-compose exec parser bash
```
- Находясь в контейнере, запустить скрипт с одним из доступных параметров:
```
python news_parser.py                       <<< вывод помощи по программе
python news_parser.py  --help            <<< вывод помощи по программе
python news_parser.py  --parse           <<< парсинг новостей
python news_parser.py  --add_resources 'examples/add_resorces.json'       <<< загрузка в БД 'resources' сайтов из файла-примера
python news_parser.py  --delete_resources 'examples/delete_resorces.json' <<< удаление из БД 'resources' сайтов по resource_id из файла-примера
```

## Формат данных для загрузки/модификаци ресурсов:
Данные о ресурсах загружаются из файла в формате json
Данные для загрузки  - это список (list) ресурсов. При этом параметры самого ресурса должны быть представлены в виде словаря (dict).

Пример:
```
[
    {
        "RESOURCE_NAME": "nur.kz",
        "RESOURCE_URL": "https://www.nur.kz",
        "top_tag": ["a", {"class": "post-preview-text js-article-link"}],
        "bottom_tag": ["div", {"class": "formatted-body io-article-body"}], 
        "title_cut": ["h1", {"class": "main-headline js-main-headline"}],
        "date_cut": ["time", {"class": "datetime datetime--publication"}]
    }
]
```

## Формат данных для удаления ресурсов:
Для удаления ресурсов нужно передать в программу файл со списком (list) id ресурсов, которые нужно удалить.
Пример:
```
[1, 2, 4, 13]
```

## О программе:

Лицензия: BSD 3-Clause License

Автор: Константин Харьков