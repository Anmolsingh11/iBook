from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.db import models

from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
CHOICES=(
    ('Biography','Biography'),
    ('Comic','Comic'),
    ('Crime','Crime'),
    ('Drama','Drama'),
    ('Fantasy','Fantasy'),
    ('History','History'),
    ('Horror','Horror'),
    ('Poetry','Poetry'),
    ('Romance','Romance'),
    ('Mystery','Mystery'),
)

class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='owner')
    title = models.CharField(max_length=50,null=False,default='No Title')
    author =models.CharField(max_length= 50, null=False,default='No name')
    description = models.TextField(max_length=1000 , null=False,default='Null')
    price = models.FloatField(null=False, default='Not on sale')
    image1 = models.ImageField(upload_to='images/', default='No images')
    genre = MultiSelectField(choices= CHOICES , default='No Choice')
    post_date = models.DateField(blank=True,null=True)
    published = models.DateField(blank=True,null=True)


@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance = None, created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)