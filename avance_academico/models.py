from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.forms import DateField


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
    carrera_materia=models.ManyToManyField('Carrera',symmetrical=False,blank=True,default="carrera")
    Dias_cursada = (
    ("LUNES", "LUNES"), ("MARTES", "MARTES"), ("MIERCOLES", "MIERCOLES"), ("JUEVES", "JUEVES"), ("VIERNES", "VIERNES"),
    ("SABADO", "SABADO"))
    Tipo_horario=(
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00','19:00'),
        ('20:00','20:00')
    )
    dia=models.CharField(max_length=50, choices=Dias_cursada, null=True, blank=True)
    horario=models.CharField(max_length=50, choices=Tipo_horario, null=True, blank=True)

    # Relaciones

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Carrera(models.Model):
    nombre=models.CharField(max_length=200, default="nombre")
    def __str__(self):
        return f"{self.nombre}"
class Estudiante(models.Model):
    # Campos básicos
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.IntegerField(default=0)
    nombre = models.CharField(max_length=200, default="0")
    apellido = models.CharField(max_length=200, default="0")
    alta_admin = models.BooleanField()
    carreras=models.ManyToManyField('Carrera', symmetrical=False, blank=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"


class Profesor(models.Model):
    # campos basicos
    nombre_profesor = models.CharField(max_length=200, default="Nombre")
    apellido_profesor = models.CharField(max_length=200, default="Apellido")
    materias = models.ManyToManyField('Materia', symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.nombre_profesor}{self.apellido_profesor}"


class MateriaCursada(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    veces_recursada = models.IntegerField(default=0)
    aprobada = models.BooleanField(default=0)
    en_curso = models.BooleanField(default=0)

    def __str__(self):
        return f"{self.estudiante}{self.materia}"

class Calificacion(models.Model):
    materia_cursada = models.ForeignKey(MateriaCursada, on_delete=models.CASCADE)
    Tipo_examen = (
        ('PARCIAL', 'PARCIAL'),
        ('RECUPERATORIO', 'RECUPERATORIO'),
        ('FINAL', 'FINAL')
    )
    tipo = models.CharField(max_length=50, choices=Tipo_examen, null=True, blank=True)
    nota = models.DecimalField(max_digits=3, decimal_places=2)
    fecha = models.DateField()

