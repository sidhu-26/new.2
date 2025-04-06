from django.db import models

# Create your models here.

class studios(models.Model):
    name = models.CharField(max_length=225)
    address = models.TextField()
    distance = models.FloatField()

    def __str__(self):
        return self.name