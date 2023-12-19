from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Profesor name", max_length=100)
    your_secondname = forms.CharField(label="Profesor secondname", max_length=100)