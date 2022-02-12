from django import template
from shop.models import Brand

register = template.Library()


@register.inclusion_tag('shop/list_brands.html')
def show_brands():
    lists_brands = [[], [], [], []]
    brands = list(Brand.objects.all())

    length = len(brands)
    value = int(length / 4)
    leftover = length % 4

    current = 0
    count = 0
    for i in range(0, 4):
        count += value
        if leftover:
            count += 1
            leftover -= 1
        lists_brands[i] += brands[current:count]
        current = count

    return {"lists_brands": lists_brands}
