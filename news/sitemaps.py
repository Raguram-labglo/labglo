from django.contrib.sitemaps import Sitemap
from news.models import News

class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return News.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_on