from tokenize import Comment
from django import forms
from .models import Comment, Article, Photo, Topic



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'})
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'media', 'topic']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'media': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }
        
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['image']

