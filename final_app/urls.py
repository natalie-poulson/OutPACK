from django.urls import path
from django.urls import path
from .  import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
]
