# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport
import requests

def getAllImages(request, input=None):
    # Obtener datos crudos desde transport.py
    data = transport.getAllImages(input)

    # Convertir los datos crudos en objetos Card usando el translator
    images = [translator.fromRequestIntoCard(item) for item in data]

    # Si el usuario está autenticado, marcar favoritos
    if request.user.is_authenticated:
        user = get_user(request)
        favourites = {fav['name'] for fav in repositories.getAllFavourites(user)}
        for img in images:
            img.is_favourite = img.name in favourites

    return images
# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.