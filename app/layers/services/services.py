# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests

def getAllImages(input=None):
    # URL de la API de Rick y Morty
    api_url = "https://rickandmortyapi.com/api/character/"

    # Obtener datos crudos de la API
    response = requests.get(api_url, params={'name': input} if input else {})
    if response.status_code == 200:
        json_collection = response.json().get('results', [])
    else:
        json_collection = []

    # Convertir datos crudos en tarjetas (Cards)
    images = []
    for character in json_collection:
        # Obtener el nombre del primer episodio
        first_episode_url = character['episode'][0] if character['episode'] else None
        first_episode_name = "Desconocido"
        if first_episode_url:
            episode_response = requests.get(first_episode_url)
            if episode_response.status_code == 200:
                first_episode_name = episode_response.json().get('name', 'Desconocido')

        # Crear la tarjeta del personaje
        images.append({
            'name': character['name'],
            'url': character['image'],
            'status': character['status'],
            'last_location': character['location']['name'],
            'first_seen': first_episode_name  # Nombre del episodio inicial
        })

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