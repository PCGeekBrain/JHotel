from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Address(models.Model):
    street_name = models.CharField(max_length=150)
    street_number = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d+$')]) # numbers only
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d+$')]) # numbers only

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=30, blank=True, null=True, validators=[
        # For full explanation of regex see hotels/models.py
        RegexValidator(regex=r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$') 
    ])
    address = models.OneToOneField(Address, blank=True, null=True)

    avatar_social = models.URLField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
