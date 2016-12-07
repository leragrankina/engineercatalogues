from django import forms
from django.contrib import admin
from django.conf import settings

from tinymce.widgets import TinyMCE

from .models import Article, Comment

# Register your models here.


class AdminForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE)

    class Meta:
        model = Article
        fields = ['title', 'text', 'date_written']


class CommentInlines(admin.TabularInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    form = AdminForm
    inlines = (CommentInlines, )

    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js', )

admin.site.register(Article, ArticleAdmin)
