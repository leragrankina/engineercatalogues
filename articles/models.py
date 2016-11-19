from django.db import models
from datetime import datetime


class Article(models.Model):
    title = models.TextField(default='')
    text = models.TextField(default='')
    url = models.URLField(default='')
    date_written = models.DateField(default=datetime.now)

    def __repr__(self):
        return self.text + " " + self.url

