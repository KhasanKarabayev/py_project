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


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        main_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = main_category.subcategories.all()
        products = Product.objects.filter(category__in=subcategories)

        return products

        # Альтернатива
        # data = []
        # for category in subcategories:
        #     products = category.products.all() # Вернет тип данный QuerySet
        #     for products in products:
        #         data.append(products)
        # return data