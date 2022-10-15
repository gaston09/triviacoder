from django.urls import path
from apptrivia.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path ("", inicio ),
    path ("home", home ),
    path ("usuario", usuario),
    path ("cienciasnaturales/", cienciasnaturales ),
    path ("cienciassociales", cienciassociales),
    path ("tecnologia/", tecnologia),

    path ("create_usuarios/", create_usuarios),    
    path ("read_usuarios/", read_usuarios),
    path ("update_usuarios/<usuario_id>", update_usuarios),
    path ("delete_usuarios/<usuario_id>", delete_usuarios),

    path ("login/", login_request),
    path ("registro/", registro),
    path ("logout/", LogoutView.as_view (template_name = 'inicio.html'), name='Logout' ),
    path ("perfil", perfilView),
    path ("perfil/editarPerfil/", editarPerfil ),
    path ("perfil/changepass/", changepass ),
    path ("perfil/changeAvatar/", AgregarAvatar ),
    
]
