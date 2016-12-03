from django.db import models
from datetime import datetime


class Article(models.Model):
    title = models.CharField(max_length=200, default='')
    text = models.TextField(default='')
    date_written = models.DateField(default=datetime.now)

    def __repr__(self):
        return 'Article: ' + self.title + ', ' + self.text


class Comment(models.Model):
    text = models.TextField(default='')
    article = models.ForeignKey(Article)

    def __repr__(self):
        return self.text
