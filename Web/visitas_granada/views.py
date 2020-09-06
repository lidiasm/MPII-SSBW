from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Visita, Comentario, VisitaForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics
from .serializers import VisitaSerializer, ComentarioSerializer
from rest_framework.response import Response
from rest_framework import permissions
from geopy.geocoders import Nominatim
import logging

logger = logging.getLogger(__name__)

class VisitasList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer

class VisitaDetalle(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer

class ComentariosList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class ComentarioDetalle(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

def index(request):
    visitas = Visita.objects.all()
    logger.info('Listado general de visitas.')
    return render(request, "base.html", {'n_visitas':len(visitas), 'visitas':visitas})

def listado(request):
    visitas = Visita.objects.all()
    comentarios = Comentario.objects.all()
    logger.info('Listado general de visitas con comentarios.')
    return render(request, 'listado.html', {'visitas': visitas, 'comentarios':comentarios})

def visita(request, id):
    todasVisitas = Visita.objects.all()
    visita = Visita.objects.get(id=id)
    comentarios = Comentario.objects.all()
    comentarios_visita = []
    for comentario in comentarios:
        if (comentario.visita.id == id):
            comentarios_visita.append(comentario)

    logger.info('Visita en detalle.')
    return render(request, 'visita.html', {'n_visitas':len(todasVisitas), 'visita':visita, 'comentarios':comentarios_visita})

def añadir_visita(request):
    form = VisitaForm()
    if (request.method == "POST"):
        form = VisitaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info('Visita añadida correctamente.')
            messages.add_message(request, messages.SUCCESS, 'Visita añadida correctamente.')
            return redirect('index')
        else:
            logger.exception('ERROR. Los datos de la nueva visita son incorrectos.')
            messages.add_message(request, messages.ERROR, 'Los datos de la nueva visita son incorrectos.')
    # Imprime el formulario
    context = {
        'form':form
    }
	# GET o error
    return render(request, "añadir_visita.html", context)

def editar_visita(request, id):
    visita = Visita.objects.get(pk=id)
    form = VisitaForm(instance=visita)
    if (request.method == "POST"):
        form = VisitaForm(request.POST, request.FILES)
        if form.is_valid():
            nuevoNombre = form.cleaned_data.get('nombre')
            if nuevoNombre: visita.nombre = nuevoNombre
            nuevaDescr = form.cleaned_data.get('descripción')
            if nuevaDescr: visita.descripción = nuevaDescr
            nuevaFoto = form.cleaned_data.get('foto')
            if nuevaFoto: visita.foto = nuevaFoto
            visita.save()
            logger.info('Visita modificada correctamente.')
            messages.add_message(request, messages.SUCCESS, 'Visita editada correctamente.')
            # Mostramos la página de la visita
            return redirect('visita', visita.id)
        else:
            logger.exception('ERROR. Datos incorrectos. No se puedo actualizar la visita.')
            messages.add_message(request, messages.ERROR, 'Los nuevos datos de la visita son incorrectos.')
    # Imprime el formulario y le pasamos el id de la visita a editar
    context = {
        'form':form,
        'id':visita.id
    }
	# GET o error
    return render(request, "editar_visita.html", context)

def borrar_visita(request, id):
    visita = Visita.objects.get(pk=id)
    resultado = visita.delete()
    if (resultado[0] == 1):
        logger.info('Visita borrada correctamente.')
        messages.add_message(request, messages.SUCCESS, 'Visita eliminada correctamente.')
    else:
        logger.exception('ERROR. No se ha podido borrar la visita.')
        messages.add_message(request, messages.ERROR, 'No se ha podido eliminar la visita.')
    return redirect('index')

def get_coordenadas_visita(request, nombre):
    if request.method == 'GET':
        geo = Nominatim()
        resultado = geo.geocode(nombre+", Granada")
        coordenadas = [resultado.latitude, resultado.longitude]
        if (coordenadas != None):
            logger.info('Coordenadas de la visita obtenidas correctamente.')
        else:
            logger.exception('ERROR. Fallo al obtener las coordenadas de la visita.')

        return JsonResponse({'coordenadas':coordenadas})

#################################################### API REST ####################################################
@csrf_exempt
def listado_visitas(request):
    """
    Lista todas las visitas registradas o crea una nueva.
    """
    if request.method == 'GET':
        visitas = Visita.objects.all()
        serializer = VisitaSerializer(visitas, many=True)
        logger.info('BD: Listado de las visitas obtenido correctamente.')
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST' and request.user.is_staff:
        data = JSONParser().parse(request)
        serializer.data = VisitaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('BD: Visita añadida correctamente.')
            return JsonResponse(serializer.data, status=201)

        logger.exception('ERROR. Fallo al añadir una nueva visita.')
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def listado_comentarios(request):
    """
    Lista todas los comentarios registrados o crea uno nuevo.
    """
    if request.method == 'GET':
        comentarios = Comentario.objects.all()
        serializer = ComentarioSerializer(comentarios, many=True)
        logger.info('BD: Listado de los comentarios obtenido correctamente.')
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST' and request.user.is_staff:
        data = JSONParser().parse(request)
        serializer = ComentarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('BD: Visita añadida correctamente.')
            return JsonResponse(serializer.data, status=201)

        logger.exception('ERROR. Fallo al añadir un nuevo comentario.')
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def detalle_visita(request, pk):
    """
    Consulta, actualiza o elimina una visita.
    """
    try:
        visita = Visita.objects.get(pk=pk)
        logger.info('BD: Detalles de la visita obtenidos correctamente.')
    except Visita.DoesNotExist:
        logger.exception('BD: ERROR al obtener los detalles de la visita.')
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VisitaSerializer(visita)
        logger.info('BD: Detalle de la visita obtenido correctamente.')
        return JsonResponse(serializer.data)

    elif request.method == 'PUT' and request.user.is_staff:
        data = JSONParser().parse(request)
        serializer = VisitaSerializer(visita, data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('BD: Visita añadida correctamente.')
            return JsonResponse(serializer.data)

        logger.exception('BD: ERROR. Fallo al actualizar una visita.')
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE' and request.user.is_staff:
        visita.delete()
        logger.info('BD: Visita eliminada correctamente.')
        return HttpResponse(status=204)

@csrf_exempt
def detalle_comentario(request, pk):
    """
    Consulta, actualiza o elimina un comentario.
    """
    try:
        comentario = Comentario.objects.get(pk=pk)
        logger.info('BD: Detalles del comentario obtenidos correctamente.')
    except Comentario.DoesNotExist:
        logger.exception('BD: ERROR al obtener los detalles del comentario.')
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ComentarioSerializer(comentario)
        logger.info('BD: Detalle del comentario obtenido correctamente.')
        return JsonResponse(serializer.data)

    elif request.method == 'PUT' and request.user.is_staff:
        data = JSONParser().parse(request)
        serializer = ComentarioSerializer(comentario, data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('BD: Comentario actualizado correctamente.')
            return JsonResponse(serializer.data)

        logger.exception('BD: ERROR. Fallo al actualizar un comentario.')
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE' and request.user.is_staff:
        comentario.delete()
        logger.info('BD: Comentario eliminada correctamente.')
        return HttpResponse(status=204)

@csrf_exempt
def likes(request, pk):
    """
    Consulta o actualiza los Me gusta de una visita existente.
    """
    try:
        visita = Visita.objects.get(pk=pk)
        logger.info('BD: Detalles de la visita obtenidos correctamente.')
    except Visita.DoesNotExist:
        logger.exception('BD: ERROR al obtener los detalles de la visita.')
        return HttpResponse(status=404)

    if request.method == 'GET':
        logger.info('BD: Número de likes de la visita obtenido correctamente.')
        return JsonResponse({'likes':visita.likes})

    elif request.method == 'PUT':
        datos = JSONParser().parse(request)
        likes_actuales = datos['likes']
        visita.likes = likes_actuales
        visita.save()
        logger.info('BD: Número de likes actualizados correctamente.')
        return JsonResponse({'likes':visita.likes})