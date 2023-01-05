from django import forms
from news.models import (Tag, News)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name',]

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ['created_on', 'updated_on']