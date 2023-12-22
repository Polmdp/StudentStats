from django.contrib import admin
from .models import Estudiante,Materia,Profesor,MateriaCursada

admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(Profesor)
admin.site.register(MateriaCursada)
# Register your models here.
