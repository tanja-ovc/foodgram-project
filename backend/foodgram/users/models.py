from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    subscriptions_of_the_user = models.ManyToManyField(
        'User', related_name='subscriptions_to_the_user',
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
