from django.db import models
import datetime

# Create your models here.


class Image(models.Model):
    title = models.CharField(max_length=200, default="Фото")
    image = models.ImageField(upload_to='images/%Y/%m/%d/')

    def __str__(self):
        return self.title


class SubImage(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)


