from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )

    def clean(self):
        if self.user == self.subscriber:
            raise ValidationError('It is not possible to subscribe to yourself')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'user'),
                name='user_following_unique'
            ),
        )
