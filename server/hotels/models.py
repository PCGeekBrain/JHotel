from django.db import models
from django.core.validators import RegexValidator
from .libs import states
import datetime

# Create your models here.
class Country(models.Model):
    """Data on the individual contry for its page"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, help_text="The two letter contry code. (also path)")
    # Optional fields
    description = models.TextField(help_text='short description', blank=True, null=True)
    # image = models.ImageField()

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return 'name',


class City(models.Model):
    """Cities in the database"""
    slug = models.SlugField(max_length=15, unique=True)
    name = models.CharField(max_length=250, unique=True)
    country = models.ForeignKey(Country)

    """Optional fields"""
    state = models.CharField(max_length=2, choices=states.states, db_index=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/hotels/city/{}".format(self.slug)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    @staticmethod
    def autocomplete_search_fields():
        return 'name',


class Hotel(models.Model):
    path = models.CharField(max_length=100, unique=True, db_index=True, blank=True, validators=[
        RegexValidator(regex=r'\w+')
    ])
    name = models.CharField(max_length=250)
    description = models.TextField()

    """address"""
    address = models.CharField(max_length=250)
    city = models.ForeignKey(City)
    zip_code = models.CharField(max_length=5)

    """Contact information"""
    phone_number = models.CharField(max_length=50, validators=[RegexValidator(
        regex=r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$')])
    """ Regex detail: https://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number#answer-16702965
        ^\s*                #Line start, match any whitespaces at the beginning if any.
        (?:\+?(\d{1,3}))?   #GROUP 1: The country code. Optional.
        [-. (]*             #Allow certain non numeric characters that may appear between the Country Code and the Area Code.
        (\d{3})             #GROUP 2: The Area Code. Required.
        [-. )]*             #Allow certain non numeric characters that may appear between the Area Code and the Exchange number.
        (\d{3})             #GROUP 3: The Exchange number. Required.
        [-. ]*              #Allow certain non numeric characters that may appear between the Exchange number and the Subscriber number.
        (\d{4})             #Group 4: The Subscriber Number. Required.
        (?: *x(\d+))?       #Group 5: The Extension number. Optional.
        \s*$                #Match any ending whitespaces if any and the end of string.
    """
    email_address = models.EmailField(blank=True, null=True)

    def generate_path(self):
        # Remove all whitespace and get the first 100 characters
        return self.name.strip().replace(' ', '')[:100]

    def __str__(self):
        return self.name

    # generate path on saveing
    def save(self, *args, **kwargs):
        if self.name and not self.path:
            self.path = self.generate_path()
        super(Hotel, self).save(*args, **kwargs)

    # get the reservations for a spacifc date
    def totalReservations(self, date):
        if isinstance(date, datetime.date):
            return self.reservation_set.filter(date=date).count()
        else:
            return 0

    # Get all the reservatons for the current date
    def totalReservationsToday(self):
        return self.reservation_set.filter(date=datetime.date.today()).count()

