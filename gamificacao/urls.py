from django.contrib import admin
from django.urls import path
from administrador.views import login_view, home_adm_view, cadastro_view, lista_desafios_view, cadastro_desafio_view, editar_desafio_view, apagar_desafio_view, desafios_corretor_view, logout_view, lista_usuarios_view,apagar_usuario_view, editar_usuario_view, convite_corretor_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login_view, name="login"),
    path("homeadmin/", home_adm_view, name="homeadmin"),
    path("cadastro/", cadastro_view, name="cadastro"),
    path("desafios/", lista_desafios_view, name="lista_desafios"),
    path("desafios/cadastrar/", cadastro_desafio_view, name="cadastro_desafio"),
    path("desafios/<int:desafio_id>/editar/", editar_desafio_view, name="editar_desafio"),
    path("desafios/<int:desafio_id>/apagar/", apagar_desafio_view, name="apagar_desafio"),
    path("desafios/corretor/", desafios_corretor_view, name="desafios_corretor"),
    path("usuarios/", lista_usuarios_view, name="lista_usuarios"),
    path("usuarios/<int:usuario_id>/apagar/", apagar_usuario_view, name="apagar_usuario"),
     path("usuarios/<int:usuario_id>/editar/", editar_usuario_view, name='editar_usuario'),
    path('convites/', convite_corretor_view, name="convites_corretor"),
    path("logout", logout_view, name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




