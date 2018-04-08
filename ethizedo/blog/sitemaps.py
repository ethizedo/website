from django.contrib.sitemaps import Sitemap

from .models import Article
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['annuaire', 'about', 'contact','blog_liste']

    def location(self, item):
        return reverse(item)

class EthizedoSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.all()



