from django.db import models
from django import forms

class Visita(models.Model):
	nombre      = models.CharField(max_length=100)
	descripción = models.CharField(max_length=200)
	likes       = models.IntegerField(default=0)
	foto = models.FileField(upload_to='fotos', blank=True)
	# Imprime los campos de la clase
	def __str__(self):
		return self.nombre

class Comentario(models.Model):
	visita      = models.ForeignKey(Visita, on_delete=models.CASCADE)
	texto       = models.CharField(max_length=500)
	# Imprime los campos de la clase
	def __str__(self):
		return self.texto

class VisitaForm(forms.ModelForm):
	class Meta:
		model = Visita
		fields = ['nombre', 'descripción', 'foto']
		widgets = {
			'nombre': forms.TextInput(attrs={'size': 40}),
			'descripción': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
			'foto': forms.FileInput()
		}