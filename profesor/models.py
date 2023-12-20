from django.db import models

# Create your models here.
class Profesor(models.Model):
    #campos basicos
    nombre_profesor = models.CharField(max_length=200, default="0")
    apellido_profesor = models.CharField(max_length=200, default="0")
    materias = models.ManyToManyField('Materia', symmetrical=False, blank=True)
    def __str__(self):
        return f"{self.nombre_profesor}{self.apellido_profesor}"
