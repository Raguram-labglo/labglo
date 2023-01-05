from django.contrib.sitemaps import Sitemap
from career.models import JobListing, Drive

class CareerSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        job_items = list(JobListing.objects.filter(is_active=True))
        drive_items = list(Drive.objects.filter(is_active=True))
        items = job_items + drive_items
        return items

    def lastmod(self, obj):
        return obj.updated_on
