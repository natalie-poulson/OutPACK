from django.urls import path
from .  import views

app_name = "final_app"

urlpatterns = [
    path('', views.landing, name='landing'),

    path('profile/create', views.profile_create, name='profile_create'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile', views.profile_view, name="profile"),


]
