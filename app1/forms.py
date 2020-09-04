from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

from .models import Book


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20, help_text='User Name' , widget=forms.TextInput(attrs={'placeholder':'User Name'}))
    first_name = forms.CharField(max_length=20, help_text='First Name' , widget=forms.TextInput(attrs={'placeholder':'First Name*'}))
    last_name = forms.CharField(max_length=20 , help_text='Last Name', widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(max_length=30 , help_text= 'Email' , widget=forms.TextInput(attrs={'placeholder':'Email*'}))
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Password*'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email','first_name', 'last_name',
                 'password1', 'password2')

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

class BookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Title of your Book"}))
    author = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Author"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Description"}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': "Price"}))
    genre = MultiSelectField(choices=CHOICES)
    image1 = forms.ImageField(help_text='max. 3 megabytes', widget=forms.FileInput(attrs={'accept': "image/*"}),required=True)

    class Meta:
        model = Book
        fields = ('title','author','description','price','genre','image1','published')


class BookUpdate(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title','author','description','price','genre','image1')