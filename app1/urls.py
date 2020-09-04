from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views
from .views import RegistrationView, VerificationView

app_name = 'app1'

urlpatterns = [
    path('', views.index , name='index'),
    path('register/', RegistrationView.as_view() , name='register'),
    path('activate/<uidb64>/<token>/',VerificationView.as_view(), name='activate'),
    path('login/', views.login,name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name ='app1/logout.html'), name='logout'),
    path('post/', views.post , name='post'),
    path('update/<int:id>', views.update , name='update'),
    path('detail/<int:id>', views.detail , name='detail'),
    path('delete/<int:id>', views.delete , name='delete'),
    path('my_ads/', views.my_ads , name='my_ads'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)