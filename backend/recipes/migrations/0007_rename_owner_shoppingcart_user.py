# Generated by Django 5.0.3 on 2024-03-12 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_rename_users_who_add_it_shopping_cart_recipe_is_in_shopping_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='owner',
            new_name='user',
        ),
    ]
