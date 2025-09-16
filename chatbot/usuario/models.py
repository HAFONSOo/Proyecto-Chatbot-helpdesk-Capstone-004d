from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.username} - {self.rut}"