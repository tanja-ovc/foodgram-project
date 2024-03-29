# Generated by Django 2.2.16 on 2022-03-08 13:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_auto_20220307_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='в избранном у'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='in_shopping_cart_of',
            field=models.ManyToManyField(blank=True, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='в списке покупок у'),
        ),
    ]
