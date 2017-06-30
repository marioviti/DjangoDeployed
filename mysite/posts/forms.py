from django import forms
from .models import Post, Article

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','image']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','abstract','image','notebook']
