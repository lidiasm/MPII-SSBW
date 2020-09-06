from django.urls import path
from . import views
from django.urls import include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # Autenticación
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # URLs para hacer consultas a través de la API REST
    path('api/visitas', views.listado_visitas, name='visitas'),
    path('api/visita/<int:pk>/', views.detalle_visita, name='detalle_visita'),
    path('api/comentarios', views.listado_comentarios, name='comentarios'),
    path('api/comentario/<int:pk>/', views.detalle_comentario, name='detalle_comentario'),
    # URL para hacer consultas/actualizaciones del campo 'likes' de visitas
    path('api/likes/<int:pk>', views.likes, name='likes'),
    # URL para conocer las coordenadas de la visita
    path('get_coordenadas_visita/<str:nombre>', views.get_coordenadas_visita, name='get_coordenadas_visita'),

    # URLs de la app
    path('listado', views.listado, name='listado'), # Muestra el listado de visitas a través de la clase Views
    path('visita/<int:id>', views.visita, name='visita'),
    path('añadir_visita', views.añadir_visita, name='añadir_visita'),
    path('editar_visita/<int:id>', views.editar_visita, name='editar_visita'),
    path('borrar_visita/<int:id>', views.borrar_visita, name='borrar_visita'),

    # URLs de las clases Serializers para listar visitas y comentarios
    path('lista_visitas/', views.VisitasList.as_view(), name='lista_visitas'),
    path('lista_comentarios/', views.ComentariosList.as_view(), name='lista_comentarios'),
    path('visita_detalle/<int:pk>/', views.VisitaDetalle.as_view(), name='visita_detalle'),
    path('comentario_detalle/<int:pk>/', views.ComentarioDetalle.as_view(), name='comentario_detalle'),
]