from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from home.models import City


class HomeSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)


class CitySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return City.objects.exclude_empty_images()

    def lastmod(self, obj):
        if hasattr(obj, "current"):
            return obj.current.updated_at

    def location(self, item):
        return reverse("city", kwargs={"pk": item.pk})
