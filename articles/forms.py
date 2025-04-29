from tokenize import Comment
from django import forms
from .models import Comment, Article

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Переконайтеся, що це модель Comment, а не рядок
        fields = ['content']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

