from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Materia(models.Model):
    Tipo_cursada = (
        ('ANUAL', 'ANUAL'),
        ('PRIMER CUATRIMESTRE', 'PRIMER CUATRIMESTRE'),
        ('SEGUNDO CUATRIMESTRE', 'SEGUNDO CUATRIMESTRE')
    )
    # Campos básicos
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    anio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    duracion = models.CharField(max_length=50, choices=Tipo_cursada, null=True, blank=True)
    # Relaciones
    correlativas = models.ManyToManyField('self', symmetrical=False, blank=True)

    # Relaciones


    def __str__(self):
        return f"{self.codigo} - {self.nombre}"