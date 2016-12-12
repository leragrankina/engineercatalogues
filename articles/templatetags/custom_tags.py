import pytz

from django import template
import datetime
from django.utils import timezone

register = template.Library()


def context_parser(context):
    article = context['article']
    request = context['request']
    user = request.user
    return {'article': article, 'user': user}


@register.inclusion_tag('articles/comment.html', takes_context=True)
def show_comment(context):
    dct = context_parser(context)
    dct['comment'] = context['comment']
    return dct


@register.inclusion_tag('articles/user_info.html', takes_context=True)
def user_info(context):
    return context_parser(context)


@register.inclusion_tag('articles/comment_form.html')
def comment_form(article):
    return {'article': article}


@register.filter(name='human_date')
def human_date(date_posted):
    delta = timezone.now() - date_posted
    secs = delta.total_seconds()
    if delta <= datetime.timedelta(minutes=1):
        return "только что"
    if delta < datetime.timedelta(hours=1):
        return '%dм назад' % (secs // 60)
    if delta < datetime.timedelta(days=1):
        return '%dч назад' % (secs // (60 * 60))
    if delta < datetime.timedelta(days=7):
        return '%dд назад' % (secs // (60 * 60 * 24))
    return date_posted.date()


