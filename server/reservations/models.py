from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Reservation(models.Model):
    """Reservation object"""
    user = models.ForeignKey(User)
    date = models.DateField()
    room = models.CharField(max_length=15)
    hotel = models.ForeignKey('hotels.Hotel')

    def __str__(self):
        return "{} {} at the {}, on {}".format(self.person_first_name, self.person_last_name, self.hotel.name, self.date)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        unique_together = ("hotel", "date", 'room')
