from django.conf import settings
from news.models import News, Tag
from blog.models import Post
from blog.models import Tag as Blog_Tag


def recaptcha(request):
    """context processor to add alerts to the site"""
    return {
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
    }

def latest_news_post(request):
    """ To get the latest bews post """
    news_lst = News.objects.filter(is_active=True).order_by("-created_on")[:3]
    result = {
        'news_post':news_lst,
    }
    return result

def news_tag_list(request):
    tag_lst = Tag.objects.all()
    result = {
        'tag_list':tag_lst,
    }
    return result

def latest_blog_post(request):
    """ To get the list of latest blog posts """
    post_lst = Post.objects.filter(is_published=True).order_by("-created_on")[:3]
    result = {
        "blog_posts":post_lst,
    }
    return result

def blog_tag_list(request):
    tag_lst = Blog_Tag.objects.all()
    result = {
        'blog_tag_list':tag_lst,
    }
    return result