from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        'подписчик',
        User, on_delete=models.CASCADE, related_name='subscriber'
    )
    user = models.ForeignKey(
        'Пользователь',
        User, on_delete=models.CASCADE, related_name='user'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        default_related_name = 'ingredient'
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'user'),
                name='user_following_unique'
            ),
        )

    def __str__(self):
        return f'{self.subscriber} to {self.user}'

    def clean(self):
        if self.user == self.subscriber:
            raise ValidationError(
                'It is not possible to subscribe to yourself'
            )
