from datetime import datetime

from django.views import View
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.urls import reverse

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
import random
import string
from .forms import RegistrationForm, BookForm, BookUpdate
from .models import Book


def randomString(stringLength=6):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

code = randomString()

def index(request):
    books = Book.objects.all().order_by('-post_date')
    return render(request,'app1/index.html',{ 'books': books })

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm
        return render(request,'app1/register.html',{'form': form})

    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            messages.success(request, "{}, Your account has been created. Now you can Login".format(username))
            user.is_active =False
            user.save()

            email_subject = 'Activate Your Account!'

            uidb64 =urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('app1:activate',kwargs={'uidb64':uidb64,'token': token_generator.make_token(user) })
            activate_url = 'http://' + domain+link
            email_body ='Hi '+first_name+', Please use this link to verify your account\n'+ activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@iBook.com',
                [email],
            )
            email.send(fail_silently=False,)

            return redirect('/login')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text((urlsafe_base64_decode(uidb64)))
            user = User.objects.get(pk = id)

            if not token_generator.check_token(user,token):
                return redirect('/login'+'?message= '+'User already activated! ')
            if user.is_active:
                return redirect('/login')
            user.is_active=True
            user.save()
            messages.success(request,'Account activated successfully!')
            return redirect('/login')

        except Exception as e:
            pass

        return redirect('/login')

@login_required(login_url='/login')
def post(request):
    book_form = BookForm()
    if request.method == 'POST':
        print("Post")
        form = BookForm(request.POST or None , request.FILES or None )
        if form.is_valid():
            print("save")
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.post_date = datetime.now()
            ad.save()
            messages.success(request, "Book posted successfully!!")
            return redirect('/')
        else:
            print(form.is_valid())
            messages.info(request, ' Please Enter Valid Details!!')
            print(form.errors)
            return render(request, 'app1/post.html', {'form': form})
    else:
        return render(request, 'app1/post.html', {'form': book_form})


def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password= password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials!!')
            return redirect('/login')
    else:
        return render(request,'app1/login.html')

@login_required(login_url='/login')
def my_ads(request):
    books = Book.objects.filter(owner = request.user)
    return render(request,'app1/my_ads.html' ,{'books': books})


@login_required(login_url='/login')
def update(request,id):
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        book.post_date = datetime.now()
        form.save()
        return redirect('/my_ads/')
    return render(request, 'app1/post.html', {'form': form, 'book': book})


@login_required(login_url='/login')
def delete(request,id):
    book = Book.objects.get(id=id)
    if request.method =='POST':
        book.delete()
        return redirect('/my_ads')
    return render(request,'app1/delete.html', {'book' :book})


def detail(request,id):
    book = Book.objects.get(id = id)
    return render(request,'app1/detail.html', {'book' :book})