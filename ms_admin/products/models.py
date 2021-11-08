from django.db import models


class User(models.Model):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)

