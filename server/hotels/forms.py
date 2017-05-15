# forms.py
from django import forms
from ajax_select import make_ajax_field
from .models import City, Country, Hotel

class CitySearchForm(forms.Form):
    city_name =  make_ajax_field(City, 'name', 'city')

class CountrySearchForm(forms.Form):
    country_name =  make_ajax_field(Country, 'name', 'country')

class HotelSearchForm(forms.Form):
    hotel_name =  make_ajax_field(Hotel, 'name', 'hotel')