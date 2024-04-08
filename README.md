# Проект 
Представляет собой платформу, где люди могут публиковать свои и не только рецепты.
Можно сформировать список покупок из понравившихся рецептов и скачать список в формате PDF

## Запуск проекта

Для запуска проекта выполните следующие шаги:

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
 # - linux
source /venv/bin/activate 
 # - windows
source /venv/Script/activate

# Установите зависимости
pip install -r requirements.txt

# Выполните миграции
python manage.py migrate

# Переименуйте файл infra/.env.example в .env
и разместите его в каталоге backend, рядом с файлом requirements.txt

# Запустите сервер
python manage.py runserver
```

## Импорт данных ингредиентов из cvs в БД

```bash
# Команда add_ingredients
# добавляет ингредиенты в базу данных. Файл .csv должен находиться 
# в каталоге data под называнием ingredients.csv
python manage.py add_ingredients 
```

## Содание тегов 

```bash
# Команда add_tags.py 
# Создает тэги в БД. Необходимые тэги прописаны в Setting.py
python manage.py add_tags
```
