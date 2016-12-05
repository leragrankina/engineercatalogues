from django import forms
from django.contrib import admin

from tinymce.widgets import TinyMCE

from .models import Article

# Register your models here.


class AdminForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE)

    class Meta:
        model = Article
        fields = ['title', 'text', 'date_written']


class ArticleAdmin(admin.ModelAdmin):
    form = AdminForm

admin.site.register(Article, ArticleAdmin)
