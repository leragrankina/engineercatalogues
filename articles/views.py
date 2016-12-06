from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy

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
        Comment(text=comment_text, article=Article.objects.get(pk=pk), created_by=request.user).save()
    return HttpResponseRedirect(reverse('articles:detail', args=(pk,)))


class CommentDelete(DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super(CommentDelete, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('articles:detail', args=(self.get_object().article.pk,))


def update_comment(request, pk):
    comment_text = request.POST.get('id_text', '')
    comment = Comment.objects.get(pk=pk)
    comment.text = comment_text
    comment.save()
    return HttpResponseRedirect(reverse_lazy('articles:detail', args=(comment.article.pk,)))
