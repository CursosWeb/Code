from django.db import models

# Create your models here.

class Contenido(models.Model):
    id = models.AutoField(primary_key=True)
    recurso = models.CharField(max_length=255, unique=True)
    contenido = models.TextField()

    def __str__(self):
        return f"{self.recurso}: {self.contenido[:50]}..."
