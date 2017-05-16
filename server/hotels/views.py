from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import Http404, JsonResponse
from django.utils.html import strip_tags, escape
from .models import City
from .forms import CitySearchForm
from datetime import datetime

# Create your views here.
def listCityHotelsHomepage(request):
    if request.method != 'POST':
        raise Http404
    form = CitySearchForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        print(form.cleaned_data)
        city = get_object_or_404(City, name=form.cleaned_data['city_name'])
        # redirect to a new URL:
        return HttpResponseRedirect('/hotels/city/{}'.format(city.slug))
    else:
        print("else", form.is_valid())
        print(request.POST)
        raise Http404

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
