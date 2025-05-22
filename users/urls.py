from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('create-user/', views.create_user, name='create_user'),
    path('login/', views.request_login, name='login'),
    path('account/', views.ProfileAboutView.as_view(), name='account'),
    path('edit-profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='edit_account'),
    path('register/', views.add_user, name='register'),
]




