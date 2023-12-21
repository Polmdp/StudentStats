from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from django.views import generic

from materia.models import Materia


class IndexView(generic.ListView):
    template_name = "avance_academico/index.html"
    context_object_name = ""
    def get_queryset(self):
        """Return the last five published questions."""
        return Materia.objects.order_by("-anio")[:50]
