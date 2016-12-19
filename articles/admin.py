from django import forms
from django.contrib import admin

from tinymce.widgets import TinyMCE
from filebrowser.fields import FileBrowseFormField

from .models import Article, Comment

# Register your models here.


class AdminForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE)
    thumbnail = FileBrowseFormField

    class Meta:
        model = Article
        fields = ['title', 'text', 'date_written', 'cover']


class CommentInlines(admin.StackedInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    form = AdminForm
    inlines = (CommentInlines, )

admin.site.register(Article, ArticleAdmin)
