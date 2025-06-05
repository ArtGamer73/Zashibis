from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Like, Topic
from .forms import ArticleForm, CommentForm, PhotoForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Відображення списку стате
@login_required
@login_required
def article_list(request):
    topic_id = request.GET.get('topic')
    topics = Topic.objects.all()
    if topic_id:
        articles = Article.objects.filter(topic_id=topic_id).order_by('-published_date')
    else:
        articles = Article.objects.all().order_by('?')  # Випадковий порядок
    return render(request, 'articles/articles_list.html', {
        'articles': articles,
        'topics': topics,
        'selected_topic': topic_id
    })

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
    topics = Topic.objects.all()  # Додаємо отримання тем
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('articles:article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/create_article.html', {'form': form, 'topics': topics})


def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author:
        return HttpResponseForbidden("You are not allowed to edit this article.")
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form, 'article': article})

# Видалення статті
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author:
        return HttpResponseForbidden("You are not allowed to delete this article.")
    if request.method == "POST":
        article.delete()
        return redirect('articles:article_list')
    return render(request, 'articles/delete_article.html', {'article': article})

@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=403)
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

#def article_list(request):
#    articles = Article.objects.all().order_by('?')  # Випадковий порядок
#    return render(request, 'articles/articles_list.html', {'articles': articles})


@require_POST
def post_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return JsonResponse({
            'status': 'ok',
            'username': request.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
        })
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

#@login_required
#class VotesView(View):
#    model = None    # Модель данных - Статьи или Комментарии
#    vote_type = None # Тип комментария Like/Dislike
# 
#    def post(self, request, pk):
#        obj = self.model.objects.get(pk=pk)
#        # GenericForeignKey не поддерживает метод get_or_create
#        try:
#            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
#            if likedislike.vote is not self.vote_type:
#                likedislike.vote = self.vote_type
#                likedislike.save(update_fields=['vote'])
#                result = True
#            else:
#                likedislike.delete()
#                result = False
#        except LikeDislike.DoesNotExist:
#            obj.votes.create(user=request.user, vote=self.vote_type)
#            result = True
# 
#        return HttpResponse(
#            json.dumps({
#                "result": result,
#                "like_count": obj.votes.likes().count(),
#                "dislike_count": obj.votes.dislikes().count(),
#                "sum_rating": obj.votes.sum_rating()
#            }),
#            content_type="application/json"
#        )