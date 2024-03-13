## Импорт данных ингредиентов из cvs или json в БД

```bash
# Команда add_ingredients_into_db принимает 1 позиционный аргумент.
# путь в проекте до файла с ингредиентами
python manage.py add_ingredients_into_db [путь к файлу]
```

## Содание тегов 

```bash
# Команда add_tags.py не принимает аргументов.
# Создает тэги в БД. Необходимые тэги прописаны в Setting.py
python manage.py add_tags
```