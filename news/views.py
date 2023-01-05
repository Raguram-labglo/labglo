from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.http import JsonResponse
from news.models import News, Tag


class NewsList(generic.ListView):
    model = News
    template_name = 'news/news_home.html'
    paginate_by = 2

    def get_queryset(self):
        tag_name = self.request.GET.get('tn', '')
        if tag_name != "":
            qset = News.objects.filter(tag__name=tag_name, is_active=True).order_by("-created_on")
        else:
            qset = News.objects.filter(is_active=True).order_by("-created_on")
        return qset

def news_details(request, slug):
    obj = get_object_or_404(News, slug=slug)
    return render(request,"news/news_details.html",
        {'news_obj': obj})
