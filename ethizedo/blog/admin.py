# -*- coding: latin-1 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Categorie, Article, ArticleAdmin, Marque, Type

admin.site.register(Categorie)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Marque)
admin.site.register(Type)

