# Generated by Django 2.2.16 on 2022-03-08 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(choices=[('BREAKFAST', 'завтрак'), ('LUNCH', 'обед'), ('DINNER', 'ужин')], unique=True, verbose_name='slug'),
        ),
    ]
