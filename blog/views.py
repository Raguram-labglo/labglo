from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from datetime import date
from blog.models import Post, Tag


class PostList(generic.ListView):
    model = Post
    template_name = 'blog/blog_home.html'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.request.GET.get('tn', '')
        if tag_name != "":
            qset = Post.objects.filter(tags__name=tag_name,
            	is_published=True).order_by("-created_on")
        else:
            qset = Post.objects.filter(is_published=True).order_by("-created_on")
        return qset

class PostDetailsView(generic.DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post_obj'

    def get_object(self):
        obj = get_object_or_404(Post, slug=self.kwargs['slug'], is_published=True)
        return obj