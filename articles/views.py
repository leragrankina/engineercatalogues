from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.urls import reverse

from .models import Article, Comment


def index(request):
    return render(request, 'index.html')


class ArticleList(ListView):
    model = Article
    template_name = 'index_articles.html'
    context_object_name = 'articles'


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article_details.html'
    context_object_name = 'article'


def save_comment(request, pk):
    comment_text = request.POST.get('comment_text', '')
    if comment_text:
        Comment(text=comment_text, article=Article.objects.get(pk=pk)).save()
    return HttpResponseRedirect(reverse('articles:detail', args=(pk,)))
