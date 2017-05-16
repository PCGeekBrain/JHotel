from ajax_select import register, LookupChannel
from .models import City, Country, Hotel

@register('city')
class CityLookup(LookupChannel):
    model = City
    def get_query(self, q, request):
        return self.model.objects.filter(name__contains=q)
    def format_match(self, item):
        return "{}, {}".format(item.name, item.country.name)
    def check_auth(self, request):
        pass

@register('country')
class CountryLookup(LookupChannel):
    model = Country
    def get_query(self, q, request):
        return self.model.objects.filter(name__contains=q)
    def check_auth(self, request):
        pass

@register('hotel')
class HotelLookup(LookupChannel):
    model = Hotel
    def get_query(self, q, request):
        return self.model.objects.filter(name__contains=q)
    def format_match(self, item):
        return "{}, {}".format(item.name, item.city.name)
    def check_auth(self, request):
        pass