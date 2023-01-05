from django.contrib.sitemaps import Sitemap
from blog.models import Post

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_on