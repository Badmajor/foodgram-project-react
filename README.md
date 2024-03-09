## Импорт данных ингрелиентов из cvs или json в БД

```bash
# Команда add_ingredients_into_db принимает 1 позиционный аргумент.
# Абсолютный путь до файла с ингредиентами
python manage.py add_ingredients_into_db [абсолютный путь к файлу]
```

## Содание тегов 

```bash
# Команда add_tags.py не принимает аргументов.
# Создает тэги в БД. Необходимые тэги прописаны в Setting.py
python manage.py add_tags
```