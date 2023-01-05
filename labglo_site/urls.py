"""labglo_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.urls import re_path as url
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.sitemaps import views
from django.urls import reverse
from django.http import HttpResponseRedirect
from career.sitemaps import CareerSitemap
from news.sitemaps import NewsSitemap
from core.sitemaps import StaticSitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'career': CareerSitemap,
    'news': NewsSitemap,
    'static': StaticSitemap,
    'blog' : PostSitemap,
}


# def handle_error(request):
#     return HttpResponseRedirect(reverse('core:home'))


urlpatterns = [
    # Admin urls
    url(r'^nimda/', admin.site.urls),

    # Adding url of django Richtext field
    url(r'^djrichtextfield/', include('djrichtextfield.urls')),
    # CKEditor urls
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # site urls
    url(r'^', include('core.urls')),
    url(r'^careers/', include('career.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^blog/', include('blog.urls')),

    # sitemaps urls
    # url(r'^sitemap\.xml$', views.index, {'sitemaps': sitemaps}),
    url(r'^sitemap\.xml$', views.sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = handle_error
# handler500 = handle_error
