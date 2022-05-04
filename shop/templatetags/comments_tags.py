from datetime import timedelta

from django.utils import timezone
from django import template

register = template.Library()


@register.simple_tag
def calc_date(date):
    delta = timezone.now() - date
    if delta < timedelta(seconds=60):
        return "Less than minute ago"
    elif delta < timedelta(minutes=60):
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif delta < timedelta(hours=24):
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta < timedelta(days=31):
        days = delta.days
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif delta < timedelta(days=365):
        months = delta.days // 31
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = delta.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
