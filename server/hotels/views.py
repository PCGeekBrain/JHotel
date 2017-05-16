from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import Http404, JsonResponse
from django.utils.html import strip_tags, escape
from .models import City, Hotel
from .forms import CitySearchForm, HotelSearchForm
from datetime import datetime

def search(request, Model, Form, data_key, field):
    form = Form(request.POST)
    if form.is_valid():
        model = Model.objects.filter(name__iexact=form.cleaned_data[data_key]).only(field)
        if model.count() == 1:
            return HttpResponseRedirect(model[0].get_absolute_url())  # redirect to the results url:
        else: # if there is more then one (or none at all)
            models = Model.objects.filter(name__icontains=form.cleaned_data[data_key])
            return render(request, 'hotels/search.html', {'models':models, "query":form.cleaned_data[data_key], "form": form})
    else:
        raise Http404 # the page request was invalid

# Show the list of hotels
def listCityHotelsSearch(request):
    if request.method == 'POST':
        return search(request, City, CitySearchForm, 'city_name', 'slug')
    else:
        return render(request, 'hotels/search.html', {"form": CitySearchForm})

# Search for hotels
def listHotelsSearch(request):
    if request.method == 'POST':
        return search(request, Hotel, HotelSearchForm, 'hotel_name', 'path')
    else:
        return render(request, 'hotels/search.html', {"form": HotelSearchForm})

#**********************individual Pages for Cities and Hotels*********************************
def updateReservations(request, slug=None, path=None):
    request_date = datetime.strptime(str(strip_tags(escape(request.POST['date']))), '%m/%d/%Y').date()
    response = {"list": []}
    if slug:
        hotels = get_object_or_404(City, slug=slug).hotel_set.all()
        for hotel in hotels:
            response['list'].append([hotel.id, hotel.totalReservations(request_date)])
    elif path:
        hotel = get_object_or_404(Hotel, path=path)
        response['list'].append([hotel.id, hotel.totalReservations(request_date)])
    return JsonResponse(response)

def listCityHotels(request, slug):
    if request.method == 'POST':
        return updateReservations(request, slug=slug)
    city = get_object_or_404(City, slug=slug)
    hotel_set = city.hotel_set.filter(verified=True)
    context = {
        "city": city,
        "hotel_set": hotel_set
    }
    return render(request, 'hotels/list_city.html', context)

def showHotel(request, path):
    if request.method == 'POST':
        return updateReservations(request, path=path)
    hotel = get_object_or_404(Hotel, path=path)
    context = {
        "hotel": hotel
    }
    return render(request, 'hotels/single_hotel.html', context)

# User adding of Hotels
def addHotel(request, slug=None):
    if slug: # If the slug is provided pass it to the template as the default value for the form item
        city = City.objects.filter(slug=slug)
    context = {
        "city": city,
        "form": None
    }
    return render(request, 'hotels/add_hotel.html')
