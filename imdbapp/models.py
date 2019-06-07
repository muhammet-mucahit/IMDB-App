from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=50)
    imdb = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.CharField(max_length=255)

