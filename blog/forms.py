from django import forms
from blog.models import Tag, Post


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name',]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'created_on', 'updated_on']
