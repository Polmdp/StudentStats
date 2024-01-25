# Generated by Django 5.0 on 2024-01-25 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avance_academico', '0002_configuracionsemestre_remove_materia_horario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='profesor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='materias_asignadas', to='avance_academico.profesor'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='materias',
            field=models.ManyToManyField(blank=True, related_name='profesores', to='avance_academico.materia'),
        ),
    ]