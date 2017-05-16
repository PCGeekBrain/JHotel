from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import Http404, JsonResponse
from django.utils.html import strip_tags, escape
from .models import City
from .forms import CitySearchForm
from datetime import datetime

# Create your views here.
def listCityHotelsSearch(request):
    if request.method == 'POST':
        form = CitySearchForm(request.POST)
        if form.is_valid():
            city = City.objects.filter(name__iexact=form.cleaned_data['city_name']).only('slug')
            if city.count() == 1:
                # redirect to a new URL:
                city = city[0]
                return HttpResponseRedirect('/hotels/city/{}'.format(city.slug))
            else: # if there is more then one (or none at all)
                cities = City.objects.filter(name__icontains=form.cleaned_data['city_name']) # inclued contains to allow for searching
                query = form.cleaned_data['city_name'] # display the query that was asked to the user
                return render(request, 'hotels/search_cities.html', {"cities": cities, "query": query})
        else:
            raise Http404 # the page request was invalid
    else:
        return render(request, 'hotels/search_cities.html')

def listCityHotels(request, slug):
    if request.method == 'POST':
        hotels = get_object_or_404(City, slug=slug).hotel_set.all()
        request_date = datetime.strptime(str(strip_tags(escape(request.POST['date']))), '%m/%d/%Y').date()
        response = {"list": []}
        for hotel in hotels:
            response['list'].append([hotel.id, hotel.totalReservations(request_date)])
        print(response)
        return JsonResponse(response)
    city = get_object_or_404(City, slug=slug)
    context = {
        "city": city
    }
    return render(request, 'hotels/list_city.html', context)
