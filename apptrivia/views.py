

from django.shortcuts import render, redirect
from django.http import HttpResponse
from apptrivia.models import Usuario, Avatar
from apptrivia.forms import AvatarFormulario, form_usuarios, UserRegisterForm, UserEditForm, ChangePasswordForm, AvatarFormulario

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def inicio(request):
    return render(request, "inicio.html")

@login_required
def home(request):
    avatar = Avatar.objects.filter (user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return render (request, 'home.html', {'avatar': avatar})

def usuario(request):
    if request.method == "POST":
        usuario =  Usuario(nombre = request.POST['nombre'], apellido = request.POST['apellido'], email = request.POST['email'])
        usuario.save()
        avatar = Avatar.objects.filter (user = request.user.id)
        try:
            avatar = avatar[0].image.url
        except:
            avatar = None
        return render (request, 'home.html', {'avatar': avatar})
    return render(request, "usuario.html")


def cienciasnaturales(request):
    return render(request, "cienciasnaturales.html")

def tecnologia(request):
    return render(request, "tecnologia.html")

def cienciassociales(request):
    return render(request, "cienciassociales.html")

def create_usuarios(request):
    if request.method == 'POST':
        usuario = Usuario (nombre = request.POST['nombre'], apellido = request.POST['apellido'], email = request.POST['email'])
        usuario.save()
        usuarios = Usuario.objects.all()
        return render (request, "usuariosCRUD/read_usuarios.html", {"usuarios": usuarios})
    return render (request, "usuariosCRUD/create_usuarios.html")


def read_usuarios(request):
    usuarios = Usuario.objects.all() #para traer toda la info
    return render (request, "usuariosCRUD/read_usuarios.html", {"usuarios": usuarios})

def update_usuarios(request, usuario_id):
    usuario= Usuario.objects.get(id = usuario_id)

    if request.method == 'POST':
        formulario = form_usuarios(request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario.nombre = informacion['nombre']
            usuario.apellido = informacion['apellido']
            usuario.email = informacion['email']
            usuario.save()
            usuarios = Usuario.objects.all() #Trae todo
            return render(request, "usuariosCRUD/read_usuarios.html", {"usuarios": usuarios})
    else:
        formulario = form_usuarios(initial={'nombre': usuario.nombre, 'apellido': usuario.apellido, 'email': usuario.email})
    return render(request,"usuariosCRUD/update_usuarios.html", {"formulario": formulario})


def delete_usuarios(request, usuario_id):
    usuario = Usuario.objects.get(id = usuario_id)
    usuario.delete()
    
    usuarios = Usuario.objects.all()
    return render (request, "usuariosCRUD/read_usuarios.html", {"usuarios": usuarios})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')

            user = authenticate(username = user, password = pwd)

            if user is not None:
                login(request, user)
                avatar = Avatar.objects.filter (user = request.user.id)
                try:
                    avatar = avatar[0].image.url
                except:
                    avatar = None
                return render (request, 'home.html', {'avatar': avatar})
            else:
                return render(request, "login.html", {'form' : form})
        else:
            return render(request, "login.html", {'form' : form})
    form = AuthenticationForm()
    return render(request, "login.html", {'form' : form})

def registro(request):
    form = UserRegisterForm(request.POST)
    if request.method =='POST':
    
        if form.is_valid():
            form.save()
            return redirect ("/apptrivia/login/")
        else:
            return render (request, "registro.html", {'form': form})
    
    form = UserRegisterForm()
    return render (request, "registro.html", {'form': form})

@login_required
def editarPerfil(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():#vamos a actualizar los siguientes datos
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            avatar = Avatar.objects.filter (user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render (request, 'home.html', {'avatar': avatar})
        else:
            avatar = Avatar.objects.filter (user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render (request, 'home.html', {'form': form, 'avatar': avatar})
    else:
        form = UserEditForm(initial={'email': usuario.email, 'username': usuario.username, 'first_name': usuario.last_name, 'email': usuario.last_name})
    return render(request, 'editarPerfil.html', {'form': form, 'usuario': usuario})

@login_required
def changepass(request):
    usuario = request.user
    if request.method == 'POST':
        # form = PasswordChangeForm (data =request.POST, user = usuario)
        form = ChangePasswordForm(data = request.POST, user = request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            avatar = Avatar.objects.filter (user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render (request, 'home.html', {'avatar': avatar[0]})
    else:
            #form = PasswordChangeForm (request.user)
            form = ChangePasswordForm(user = request.user)
    return render (request, 'changepass.html', {'form': form, 'usuario': usuario})

@login_required
def perfilView(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return render(request, 'perfil.html', {'avatar': avatar})

@login_required
def AgregarAvatar(request):
    if request.method == 'POST':
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username = request.user)
            avatar = Avatar (user = user, image = form.cleaned_data['avatar'], id = request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter (user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render (request, 'home.html', {'avatar': avatar})
    else:
        try:
            avatar = Avatar.objects.filter (user = request.user.id)
            form = AvatarFormulario()
        except:
            form = AvatarFormulario()
    return render (request, 'AgregarAvatar.html', {'form': form})
