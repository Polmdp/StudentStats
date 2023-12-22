from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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


class Estudiante(models.Model):
    # Campos básicos
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.IntegerField(default=0)
    nombre = models.CharField(max_length=200,default="0")
    apellido = models.CharField(max_length=200,default="0")
    alta_admin=models.BooleanField()
 #   materias_aprobadas = models.ManyToManyField('Materia', related_name='estudiantes_aprobados', blank=True)
#    materias_en_curso = models.ManyToManyField('Materia', related_name='estudiantes_en_curso', blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"

class Profesor(models.Model):
    #campos basicos
    nombre_profesor = models.CharField(max_length=200, default="Nombre")
    apellido_profesor = models.CharField(max_length=200, default="Apellido")
    materias = models.ManyToManyField('Materia', symmetrical=False, blank=True)
    def __str__(self):
        return f"{self.nombre_profesor}{self.apellido_profesor}"

class MateriaCursada(models.Model):
    Tipo = (
        ('ANUAL', 'ANUAL'),
        ('PRIMER CUATRIMESTRE', 'PRIMER CUATRIMESTRE'),
        ('SEGUNDO CUATRIMESTRE', 'SEGUNDO CUATRIMESTRE')
    )
    estudiante=models.ForeignKey(Estudiante,on_delete=models.CASCADE)
    materia=models.ForeignKey(Materia,on_delete=models.CASCADE)
    tipo_cursada = models.CharField(max_length=50, choices=Tipo, null=True, blank=True)
    veces_recursada=models.IntegerField(default=0)
    aprobada=models.BooleanField(default=0)
    en_curso=models.BooleanField(default=0)
    def __str__(self):
        return f"{self.estudiante}{self.materia}"