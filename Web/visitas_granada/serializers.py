from rest_framework import serializers
from .models import Visita, Comentario

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = ['id', 'nombre', 'descripción', 'likes', 'foto']

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'visita', 'texto']