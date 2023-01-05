from django.urls import re_path as url
from django.views.generic import TemplateView
from news.views import NewsList, news_details


app_name = 'news'
urlpatterns = [
    # app urls
    url(r'^$', NewsList.as_view(), name='home'),
    url(r'^(?P<slug>[\w-]+)/$', news_details, name='news_details'),

]
