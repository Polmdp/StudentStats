from django.contrib.auth.models import User
from django.db import models


class Materia(models.Model):
    # Campos básicos

    # Relaciones
    correlativas = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Estudiante(models.Model):
    # Campos básicos
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Relaciones
    materias_aprobadas = models.ManyToManyField('Materia', related_name='estudiantes_aprobados', blank=True)
    materias_en_curso = models.ManyToManyField('Materia', related_name='estudiantes_en_curso', blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.matricula})"
