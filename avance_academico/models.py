from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



class Estudiante(models.Model):
    # Campos básicos
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.IntegerField(default=0)
    nombre = models.CharField(max_length=200,default="0")
    apellido = models.CharField(max_length=200,default="0")

    # Relaciones
    materias_aprobadas = models.ManyToManyField('Materia', related_name='estudiantes_aprobados', blank=True)
    materias_en_curso = models.ManyToManyField('Materia', related_name='estudiantes_en_curso', blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"

