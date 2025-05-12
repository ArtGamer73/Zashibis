from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Like
from .forms import ArticleForm, CommentForm, PhotoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Відображення списку стате
@login_required
def article_list(request):
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'articles/articles_list.html', {'articles': articles})

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  
    else:
        form = PhotoForm()
    return render(request, 'create_article.html', {'form': form})

# Перегляд статті
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})

# Створення нової статті
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Обробка request.FILES
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'The article has been successfully created!')
            return redirect('articles:article_list') 
        else:
            messages.error(request, 'An error occurred. Please check the data you entered.')
    else:
        form = ArticleForm()
    
    return render(request, 'articles/create_article.html', {'form': form})

# Редагування статті
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)  # Обробка request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'The article has been successfully updated!')
            return redirect('articles:article_list')
        else:
            messages.error(request, 'An error occurred. Please check the data you entered.')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form})

# Видалення статті
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:article_list')
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
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                article=article,
                user=request.user,
                content=content
            )
    return redirect('articles:article_list')

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

def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        # Перевіряємо, чи існує лайк від цього користувача
        like, created = Like.objects.get_or_create(article=article, user=request.user)
        if not created:
            # Якщо лайк вже існує, видаляємо його (анлайк)
            like.delete()
    return redirect('articles:article_list')