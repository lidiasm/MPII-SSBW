import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mi_sitio_web.settings')

import django
django.setup()

from visitas_granada.models import Visita, Comentario

if __name__ == "__main__":
    # Obtenemos todas las visitas y comentarios registrados
    visitasRegistradas = Visita.objects.all()
    comentariosRegistrados = Comentario.objects.all()
    # Añadimos una nueva visita si no se encuentra ya en la base de datos
    nuevaVisita = Visita(nombre="Sierra Nevada", descripción="Texto Sierra Nevada")
    visitasIguales = 0
    for visita in visitasRegistradas:
        if (visita.nombre != nuevaVisita.nombre and visita.descripción != nuevaVisita.descripción):
            visitasIguales += 1

    if (visitasIguales == 0):
        nuevaVisita.save()
        print("Nueva visita añadida.")

    # Obtener el id de un objeto a partir de un campo, en este caso es el nombre.
    visita = Visita.objects.get(nombre='Sierra Nevada')
    print("Id de la visita Sierra Nevada: ", visita.id)

    # Añadimos el nuevo comentario si no existe préviamente
    # Con __contain el texto tiene que ser exacto para que haga match.
    # Para que sea solo una subcadena se debe utilizar __icontains
    nuevoComentario = Comentario(visita=visita, texto="Me flipa la visita!")
    busquedaTexto = Comentario.objects.filter(texto__contains=nuevoComentario.texto)

    if (not busquedaTexto):
        nuevoComentario.save()
        print("Nuevo comentario añadido")

    ### Ejemplos de consultas
    # Todos los registros
    print("Visitas: ", Visita.objects.all())
    print("\nComentarios: ", Comentario.objects.all())
    # Conjunto de un objeto por su id
    print("\nPrimera visita: ", Visita.objects.filter(id=1))
    # Un solo objeto también por su id
    print("\nSegunda visita: ", Visita.objects.get(id=visita.id))
    # Objeto que en el campo Nombre comience por 'Al'
    print("\nVisitas que empiezan por A: ", Visita.objects.filter(nombre__startswith='Al'))