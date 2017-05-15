from django.contrib import admin
from .models import Hotel, Country, City

# Register your models here.
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Hotel)
