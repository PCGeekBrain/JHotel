from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^city/(?P<slug>[-\w]+)$', views.listCityHotels),
    url(r'^citysearch/$', views.listCityHotelsSearch),
    url(r'^hotel/(?P<path>[-\w+]+)$', views.showHotel),
    url(r'^hotelsearch/', views.listHotelsSearch),
    url(r'^add/$', views.addHotel),
    url(r'^add/(?P<slug>[-\w]+)$', views.addHotel)
]