from django.urls import re_path as url
from django.views.generic import TemplateView
from blog.views import PostList, PostDetailsView


app_name = 'blog'
urlpatterns = [
    # app urls
    url(r'^$', PostList.as_view(), name='blog_home'),
    url(r'^(?P<year>[\w-]+)/(?P<month>[\w-]+)/(?P<day>[\w-]+)/(?P<slug>[\w-]+)/$', PostDetailsView.as_view(), name='post_details'),
]
