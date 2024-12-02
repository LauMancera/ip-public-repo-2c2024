# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib  import messages
def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    # Llamar al services para obtener las imágenes, pasando el request
    images = services.getAllImages(request)
    # Obtener favoritos del usuario (si aplica)
    favourite_list = []
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })
def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        pass
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)  
    return redirect('login')
def register(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Verificar si las contraseñas coinciden
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')  # Vuelve al formulario de registro

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register')  # Vuelve al formulario de registro

        # Verificar si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('register')  # Vuelve al formulario de registro

        # Crear el nuevo usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Mostrar un mensaje de éxito
        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect('home')  

    # Si el método no es POST, renderizar la página de registro
    return render(request, 'registration/register.html')
