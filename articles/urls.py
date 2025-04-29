from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='article_list'),  # Список статей
    path('article/<int:pk>/', views.article_detail, name='article_detail'),  # Окрема стаття
    path('create/', views.create_article, name='create_article'),
    path('edit/<int:pk>/', views.edit_article, name='edit_article'),  # Редагування статті
    path('delete/<int:pk>/', views.delete_article, name='delete_article'),  # Видалення статті
    path('search/', views.search_articles, name='search_articles'),  # Пошук статей
]