from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from filebrowser.fields import FileBrowseField
from filebrowser.settings import ADMIN_THUMBNAIL


class Article(models.Model):
    title = models.CharField(max_length=200, default='')
    text = models.TextField(default='', blank=True)
    date_written = models.DateField(default=timezone.now)
    cover = FileBrowseField("Image", max_length=200, directory="/uploads", blank=True)

    def __str__(self):
        return self.title

    @property
    def thumbnail(self):
        if self.cover:
            return self.cover.version_generate(ADMIN_THUMBNAIL).url
        return ""


class Comment(models.Model):
    text = models.TextField(default='')
    article = models.ForeignKey(Article)
    created_by = models.ForeignKey(User)
    datetime_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-datetime_posted']
