from django.shortcuts import render
from main.models import Article


def index(request):
    return render(request, 'index.html')


def articles_list(request):
    return render(request, 'index_articles.html', {'articles': Article.objects.all()})


def catalogues_list(request):
    return render(request, 'catalog.html')


def article_page(request, page):
    return render(request, page + ".html")
