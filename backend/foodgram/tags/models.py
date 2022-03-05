from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=20, verbose_name='название', unique=True
    )
    color = models.CharField(
        max_length=7, verbose_name='цвет (HEX-код)', unique=True
    )
    slug = models.SlugField(verbose_name='slug', unique=True)

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.name
