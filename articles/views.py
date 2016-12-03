from django.shortcuts import render
from articles.models import Article, Comment


def index(request):
    return render(request, 'index.html')


def articles_list(request):
    return render(request, 'index_articles.html', {'articles': Article.objects.all()})


def catalogues_list(request):
    return render(request, 'catalog.html')


def article_detail(request, art_url):
    comment_text = request.POST.get('comment_text', '')
    if comment_text:
        comment = Comment(text=comment_text)
        comment.save()
    return render(request, 'article_details.html', {'article': Article.objects.get(url=art_url),
                                                    'comments': Comment.objects.all()})
