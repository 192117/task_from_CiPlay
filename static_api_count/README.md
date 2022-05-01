# Микросервис для счетчиков статистики.

В сервисе используется SQLite3.

## Установка и запуск:

1. Клонировать репозиторий
    ```
    git clone 
    ```
2. Переходим в директорию task_from_CiPlay\static_api_count
    ```
    cd task_from_CiPlay\static_api_count
    ```
3. Создаем виртуальное окружение, активируем и устанавливаем зависимости
    ``` 
    python -m venv venv
    ```
    ```
    pip install -r requirements.txt
    ```
4. Выполняем в командной строке
   ```
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```
5. Создаем в директории task_from_CiPlay\static_api_count\static_api_count файл _**.env**_
и записываем туда полученный ключ в формате:
   ```
   SECRET_KEY = 'полученный ключ'
   ```
   или используйте данный ключ:
   ```
   SECRET_KEY = 't0(m08#x-u+1gkopy+4er9xs@%qfe4@5vi6&yc9ecc-my3&!!5'
   ```
6. Применяем миграции
   ```
   python manage.py migrate
   ```
7. Можно создать суперпользователя (можно пропустить данный шаг)
   ```
   python manage.py createsuperuser
   ```
8. Запускаем приложение
   ```
   python manage.py runserver
   ```
9. Сервис доступен по адресу 
   ```
   http://127.0.0.1:8000/
   ```
   
## Описание работы:

- ### Добавляем данные в БД:

Делаем POST запрос по адресу:

```
http://127.0.0.1:8000/api/v1/save/
```

Параметры запроса:

```
{
    date: string(date) - Дата события. Обязательный параметр.
    views: integer - Количество показов. Необязательный параметр.
    clicks:	integer - Количество кликов. Необязательный параметр.
    cost:	string(decimal) - Стоимость кликов. Необязательный параметр.
}
```

После запроса происходит проверка на валидность параметров. А именно views/clicks/cost при наличии проверяются, что 
неотрицательные. А поле date проверяется на корректность: день (1-31), месяц (01-12), год (1000-2999)

При успешном запросе ответ представляет собой:

```
{
    "date": "YYYY-MM-DD",
    "views": Переданное число или null (при отсутствии в запросе),
    "clicks": Переданное число или null (при отсутствии в запросе),
    "cost": "Переданное число с точностью до 2 знака или null (при отсутствии в запросе)"
}
```

В случае невалидности views/clicks/cost ответ будет:

```
{
    "views/clicks/cost": [
        "Must be non-negative"
    ]
}
```

В случае невалидности date ответ будет:

```
{
    "date": [
        "Incorrect date!"
    ]
}
```

- ### Просмотр данных:

Делаем GET запрос по адресу:

```
http://127.0.0.1:8000/api/v1/show/from_date/to_date/?ordering=param
```

где вместо from_date и to_date указываем интересующие нас даты в формате **_YYYY-MM-DD_** 

в поле _ordering_ можно указать сортировку по любому из полей ответа. (В случае отсутствия сортировка будет по дате от 
свежих к старым данным)

Пример ответа на запрос 
```
http://127.0.0.1:8000/api/v1/show/1999-01-01/2010-05-05/?ordering=date
```
```
[
    {
        "date": "1999-01-01",
        "views": 5,
        "clicks": 5,
        "cost": "5.00",
        "cpc": "1.00",
        "cpm": "1000.00"
    },
    {
        "date": "1999-02-01",
        "views": 5,
        "clicks": 5,
        "cost": "5.00",
        "cpc": "1.00",
        "cpm": "1000.00"
    },
    {
        "date": "1999-03-01",
        "views": 5,
        "clicks": 5,
        "cost": "5.00",
        "cpc": "1.00",
        "cpm": "1000.00"
    }
]
```

- ### Удалить все данные:

Делаем GET запрос по адресу:

```
http://127.0.0.1:8000/api/v1/clear/
```

Ответ на запрос будет:

```
[]
```