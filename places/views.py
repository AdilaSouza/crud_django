from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Places
from django.utils import timezone
from django.db import connection

def index(request, important_message=None):
    print("debug")
    print(connection.queries)
    print(Places.objects.order_by('-create_date').query)
    print("debug")
    place_list = Places.objects.order_by('-create_date')
    print(place_list)
    context = {'place_list': place_list}
    return render(request, 'places/index.html', context)


def detail(request, place_id=''):
    place_selected = {"id": ''}
    if(place_id != ''):
        place_selected = Places.objects.get(id=place_id)

    return render(request, 'places/detail.html', {'place': place_selected})


def delete(request, place_id):
    try:
        place2Delete = Places.objects.get(pk=place_id)
        place2Delete.delete()
        return render(request, 'places/delete.html', {
            'place': place2Delete,
            'important_message': "Seu registro foi apagado com sucesso.",
        })
    except (KeyError, Places.DoesNotExist):
        return render(request, 'places/delete.html', {
            'place': place2Delete,
            'important_message': "Houve um erro ao apagar o registro.",
        })


def upsert(request):
    _id = request.POST['id']
    _name = request.POST['name']
    _address_state = request.POST['address_state']
    _address_city = request.POST['address_city']
    _address_neighborhood = request.POST['address_neighborhood']
    _image_url = request.POST['image_url']

    if(_id == ''):
        try:
            newPlace = Places(
                address_state = _address_state,
                address_city = _address_city,
                address_neighborhood = _address_neighborhood,
                name=_name, 
                image_url = _image_url,
                create_date=timezone.now())

            newPlace.save()

            return render(request, 'places/detail.html', {
                'place': newPlace,
                'important_message': "O registro foi salvo com sucesso.",
            })
        except (KeyError, Places.DoesNotExist):
            return render(request, 'places/detail.html', {
                'place': newPlace,
                'important_message': "Não foi possivel salvar o registro.",
            })

    else:
        try:
            place2Update = Places.objects.get(pk=_id)
            place2Update.name = _name
            place2Update.address_state = _address_state
            place2Update.address_city = _address_city
            place2Update.address_neighborhood = _address_neighborhood
            place2Update.image_url = _image_url

            place2Update.save()
            return render(request, 'places/detail.html', {
                'place': place2Update,
                'important_message': "O registro foi atualizado com sucesso.",
            })
        except (KeyError, Places.DoesNotExist):
            return render(request, 'places/detail.html', {
                'place': newPlace,
                'important_message': "Não foi possivel atualizar o registro.",
            })
