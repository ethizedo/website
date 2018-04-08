#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django import forms
from django_comments.moderation import CommentModerator, moderator
import django_filters
from django.db import models
from django_comments.abstracts import CommentAbstractModel

class CommentAnswer(CommentAbstractModel):
    parent = models.ForeignKey('self', null=True, related_name='replies')



class Article(models.Model):
    titre = models.CharField(max_length=500)
    slug = models.SlugField(max_length=100)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de parution")
    categorie = models.ManyToManyField('Categorie')
    image = models.CharField(max_length=500)
    meta_description = models.CharField(max_length=200)

    def get_absolute_url(self):
        return '/article/'+self.slug+'/'


    def __unicode__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.titre



class Categorie(models.Model):
    nom = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100)
    def __str__(self):
        return self.nom

class ArticleAdmin(admin.ModelAdmin):
   list_display   = ('titre', 'date')
   date_hierarchy = 'date'
   ordering       = ('date', )
   search_fields  = ('titre', 'contenu')
   prepopulated_fields = {'slug': ('titre', ), }

class Marque(models.Model):
   nom=models.CharField(max_length=300)
   url=models.URLField()
   slug=models.SlugField(max_length=100)
   contenu=models.CharField(max_length=380)
   reduction=models.TextField(null=True, blank=True)
   image=models.CharField(max_length=500, blank=True, null=True)
   categorie=models.ForeignKey('Categorie')
   types=models.ManyToManyField('Type')
   def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.nom

class Type(models.Model):
   nom=models.CharField(max_length=200)
   image=models.CharField(max_length=500)
   def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.nom


class ProductFilter(django_filters.FilterSet):
  types = django_filters.ModelMultipleChoiceFilter(queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple, conjoined=True)
  class Meta:
    model = Marque
    fields = ['types']



class EntryModerator(CommentModerator):
  auto_approve_for_superusers = False
  email_notification = True

moderator.register(Article, EntryModerator)




