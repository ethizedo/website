#-*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import ListView
from .models import Article
from django_filters.views import FilterView
from blog.models import ProductFilter
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap


from .sitemaps import EthizedoSitemap
from .sitemaps import StaticSitemap

from . import views

sitemaps = {
   'ethizedo': EthizedoSitemap(),
   'static': StaticSitemap(),
}


urlpatterns = [
	#url(r'^$', ListView.as_view(model=Article,
    #                context_object_name="derniers_articles",
    #                template_name="blog/accueil.html")),
	url(r'^$', views.ListeArticles.as_view(), name="blog_liste"),
    url(r'^article/(?P<slug>.+)$', views.view_article, name='article'),  # Vue d'un article
    #url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})$', views.ListeArticlesFilter.as_view()), #cherche un article par année et mois
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^categorie/(?P<slug>.+)$', views.ListeArticlesFilter.as_view(), name='blog_categorie'),
    url(r'^about$', views.about, name='about'),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^comments/post/', views.comment),
    url(r'^annuaire/$', RedirectView.as_view(url='/annuaire-de-la-mode-ethique/')),
    url(r'^annuaire-de-la-mode-ethique/$', views.Annuaire.as_view(), name='annuaire'),
    url(r'^search/$', views.Annuaire.as_view(), name='search'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    ]
