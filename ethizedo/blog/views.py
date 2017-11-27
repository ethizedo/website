#-*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, Http404
from datetime import datetime
from django.shortcuts import render
from blog.models import Article
from blog.models import Categorie
from blog.models import Marque
from blog.models import Type
from django.shortcuts import get_list_or_404, get_object_or_404
from .forms import ContactForm
from django.utils import timezone
from blog.models import ProductFilter
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/form.html', locals())


class ListeArticles(ListView):
    #model = Categorie
    model=Article
    context_object_name = "derniers_articles"
    template_name = "blog/firstpage.html"
    paginate_by=3
    #lte : less or equal than 
    #queryset=Article.objects.filter(date__lte=timezone.now()).order_by('-date')[0:3]
    #queryset = Article.objects.filter(categorie__id=1)

    # usefull if we want to pass in url "id/3" for example
    def get_queryset(self):
        context=Article.objects.filter(date__lte=timezone.now()).order_by('-date')
        #context['all_articles']=Article.objects.filter(date__lte=timezone.now()).order_by('-date')
        #context['categories']=Categorie.objects.all()
        return context


    def get_context_data(self, **kwargs):
        # Nous récupérons le contexte depuis la super-classe
        context = super(ListeArticles, self).get_context_data(**kwargs)
        # Nous ajoutons la liste des catégories, sans filtre particulier
        context['categories']= Categorie.objects.all()
        context['all_articles']=Article.objects.filter(date__lte=timezone.now()).order_by('-date')
        return context


class ListeArticlesFilter(ListView):
    model = Article
    context_object_name = "derniers_articles_2"
    template_name = "blog/categorie.html"
    paginate_by=5
    def get_queryset(self):
        return Article.objects.filter(categorie__slug=self.kwargs['slug'])

class Annuaire(ListView):
    model=Marque
    context_object_name="marques"
    template_name="blog/annuaire.html"
    paginate_by=30
    def get_queryset(self):
        return Marque.objects.all()

    def get_context_data(self, **kwargs):
        context=super(Annuaire, self).get_context_data(**kwargs)
        context['marque']=Marque.objects.all()
        #context['filter']=Marque.objects.filter(types__nom=self.kwargs['types'])
        context['filter']=ProductFilter(self.request.GET, queryset=Marque.objects.all())
        #context['marque2']=Marque.objects.filter(filtre)
        return context


def view_article(request, slug):
    """ Afficher un article complet """
    article = get_object_or_404(Article, slug=slug)
    try:
        next_article = article.get_next_by_date()
    except Article.DoesNotExist:
        next_article = None

    try:
        previous_article = article.get_previous_by_date()
    except Article.DoesNotExist:
        previous_article = None
        print previous_article

    return render(request, 'blog/lire.html', {
        'article': article,
        'next_article': next_article,
        'previous_article': previous_article
    })
    

def list_articles(request, month, year):
    """ Liste des articles d'un mois précis. """
    return HttpResponse(
        "Vous avez demandé les articles de {0} {1}.".format(month, year)  
    )

def about(request):
    return render(request, 'blog/about.html')

def comment(request):
    # Redirecting after comment submission
    return HttpResponseRedirect(request.POST['next'])

def search(request):
    marque_list = Marque.objects.all()
    marque_filter = ProductFilter(request.GET, queryset=marque_list)
    return render(request, 'blog/annuaire.html', {'filter': marque_filter})
