from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name} ({self.code})'
