from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^city/(?P<slug>[-\w]+)', views.listCityHotels),
    url(r'^citysearch/', views.listCityHotelsSearch),
]