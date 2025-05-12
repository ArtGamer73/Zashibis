from django.urls import path, include
from . import views  

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),  # Головна сторінка блогу
    #path('', include('articles.urls')),
]


