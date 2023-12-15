from django.shortcuts import render

# Create your views here.

from django.views import generic
from .models import Materia


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Materia.objects.order_by("anio")[:50]