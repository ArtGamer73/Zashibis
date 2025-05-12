from django.shortcuts import render
from articles.models import Article

def home(request):
    articles = Article.objects.all().order_by('-published_date')  # Отримуємо всі статті
    return render(request, 'home/home.html', {'articles': articles})