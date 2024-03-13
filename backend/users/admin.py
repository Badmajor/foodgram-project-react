from django.contrib import admin
from django.contrib.auth import get_user_model, models
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

admin.site.unregister(models.User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = ("username", "email",)


admin.site.unregister(models.Group)
