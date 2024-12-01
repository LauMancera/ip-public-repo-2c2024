# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
    pass
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
        if password == password2:
            # Verificar si el nombre de usuario ya está en uso
            if User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya está en uso.")
                return redirect('register')

            # Verificar si el correo electrónico ya está registrado
            elif User.objects.filter(email=email).exists():
                messages.error(request, "El correo electrónico ya está registrado.")
                return redirect('register')

            else:
                # Crear el nuevo usuario con los campos adicionales
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name  # Asignar nombre
                user.last_name = last_name    # Asignar apellido
                user.save()

                # Mensaje de éxito
                messages.success(request, "Registro exitoso. Puedes iniciar sesión ahora.")
                return redirect('login')  # Redirige al login después de registrar
        else:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')  # Vuelve a la página de registro si hay error
    else:
        return render(request, 'registration/register.html')

