from dataclasses import fields
from django import forms
from .models import InfoMed, admin_indi, demanda_diarias
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class InfoMedForm(forms.ModelForm):
    class Meta:
        model = InfoMed
        fields=["codigo", "nombre", "concentracion", "presentacion"]


class MedicamentoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Medicamento', max_length=50)


class DemandaForm(forms.ModelForm):

    class Meta:
        model = demanda_diarias
        fields = ['entregado', 'no_entregado', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


class admin_indiForm(forms.ModelForm):
    class Meta: 
        model = admin_indi
        fields=['codigo', 'nombre', 'metaIndi']


class DateRangeForms(forms.Form):
    fecha_inicio = forms.DateField(label="Fecha de inicio")
    fecha_fin = forms.DateField(label="Fecha de fin")


class FechaForm(forms.Form):
    mes = forms.IntegerField()
    ano = forms.IntegerField()


class DateRangeForm(forms.Form):
    fecha_inicio = forms.DateField(label="Fecha de inicio")
    fecha_fin = forms.DateField(label="Fecha de fin")



