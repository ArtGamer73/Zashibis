from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required

# Відображення списку статей
def article_list(request):
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'articles/articles_list.html', {'articles': articles})

# Перегляд статті
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/articles_detail.html', {'article': article})

# Створення нової статті
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Призначаємо автора статті
            article.save()
            messages.success(request, 'Статтю успішно створено!')
            return redirect('articles:article_list')  # Замініть на ім'я вашого URL для списку статей
        else:
            messages.error(request, 'Виникла помилка. Перевірте введені дані.')
    else:
        form = ArticleForm()
    
    return render(request, 'articles/create_article.html', {'form': form})

# Редагування статті
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form, 'article': article})

# Видалення статті
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/delete_article.html', {'article': article})

# Пошук статей
def search_articles(request):
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(title__icontains=query)
    else:
        articles = Article.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

# Відображення статті з коментарями
def article_with_comments(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()
    return render(request, 'articles/article_with_comments.html', {'article': article, 'comments': comments})

# Додати коментар до статті
def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_with_comments', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'articles/add_comment.html', {'form': form, 'article': article})

# Редагування коментаря
def edit_comment(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('article_with_comments', pk=article.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'articles/edit_comment.html', {'form': form, 'article': article, 'comment': comment})

