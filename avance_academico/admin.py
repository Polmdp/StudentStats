from django.contrib import admin
from .models import Estudiante,Materia,Profesor,MateriaCursada,Calificacion,ConfiguracionSemestre

admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(Profesor)
admin.site.register(MateriaCursada)
admin.site.register(Calificacion)
admin.site.register(ConfiguracionSemestre)
# Register your models here.
