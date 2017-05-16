from django.shortcuts import render
# from django.views.generic import TemplateView
from hotels.forms import HotelSearchForm, CitySearchForm

def home_page(request):
    context = {
        "city_form": CitySearchForm,
        "hotel_form": HotelSearchForm
    }
    return render(request, 'homepage/index.html', context=context)

