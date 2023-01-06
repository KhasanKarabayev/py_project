from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product


class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    extra_context = {
        'title': 'Главная страница'
    }
    template_name = 'shop/product_list.html'

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories