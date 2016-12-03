from django.shortcuts import render, get_object_or_404

from .models import Article, Comment


def index(request):
    return render(request, 'index.html')


def articles_list(request):
    return render(request, 'index_articles.html', {'articles': Article.objects.all()})


def catalogues_list(request):
    return render(request, 'catalog.html')


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comment_text = request.POST.get('comment_text', '')
    if comment_text:
        comment = Comment(text=comment_text, article=article)
        comment.save()
    return render(request, 'article_details.html', {'article': article,
                                                    'comments': article.comment_set.all()})
