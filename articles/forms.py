from tokenize import Comment
from django import forms
from .models import Comment, Article, Photo

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['image']