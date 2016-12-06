from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200, default='')
    text = models.TextField(default='')
    date_written = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(default='')
    article = models.ForeignKey(Article)
    created_by = models.ForeignKey(User)
    datetime_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
