
# Проект FoodGram
Пердставляет собой платформу, где люди могут публиковать свои и не только рецепты.
Всегда можно найти интересный рецепт и скачать список необходимых ингредиентов, в виде списка покупок.

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

# Запустите сервер
python manage.py runserver
```

## Импорт данных ингредиентов из cvs или json в БД

```bash
# Команда add_ingredients_into_db 
# добавляет ингредиенты в базу данных. Файл должен находиться 
# в каталоге data и называться ingredients
# принмает разрещения .json и .csv
python manage.py add_ingredients 
```

## Содание тегов 

```bash
# Команда add_tags.py 
# Создает тэги в БД. Необходимые тэги прописаны в Setting.py
python manage.py add_tags
```