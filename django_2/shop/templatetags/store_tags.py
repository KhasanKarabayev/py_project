from django import template
from shop.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)


@register.simple_tag()  # Первый способ усложненный, для типов часов (механика или авто)
def get_subcategories(category):
    return Category.objects.filter(parent=category)


@register.simple_tag()  # Второй простой способ, менее усложненный (цена, цвет, размер)
def get_sorted():
    title = "По цене"
    title2 = "По цвету"
    title3 = "По размеру"
    price1 = "По возрастанию цены"
    price2 = "По убыванию цены"
    color1 = "От А до Я"
    color2 = "От Я до А"
    size1 = "По возрастанию размера"
    size2 = "По убыванию размера"
    sorters = [
        {
            'title': title,
            'sorters': [
                ('price', price1),
                ('-price', price2)
            ]
        },
        {
            'title': title2,
            'sorters': [
                ('color', color1),
                ('-color', color2)
            ]
        },
        {
            'title': title3,
            'sorters': [
                ('size', size1),
                ('-size', size2)
            ]
        }
    ]

    return sorters
