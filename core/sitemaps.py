from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ['core:home', 'core:contact', 'core:about_us',
                'core:services', 'core:gallery', 'core:amazon-affiliate']

    def location(self, item):
        return reverse(item)
