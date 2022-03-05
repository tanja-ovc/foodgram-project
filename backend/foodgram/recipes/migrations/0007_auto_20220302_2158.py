# Generated by Django 2.2.16 on 2022-03-02 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20220302_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='is_favorited',
            field=models.BooleanField(default=False, verbose_name='в вашем избранном'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='is_in_shopping_cart',
            field=models.BooleanField(default=False, verbose_name='в вашем списке покупок'),
        ),
    ]
