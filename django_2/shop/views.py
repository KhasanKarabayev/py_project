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
        sort_field = self.request.GET.get('sort')  # цена, цвет, размер
        type_field = self.request.GET.get('type')  # Автоматические, механические
        if type_field:
            products = Product.objects.filter(category__slug=type_field)
            return products

        main_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = main_category.subcategories.all()
        products = Product.objects.filter(category__in=subcategories)

        if sort_field:
            products = products.order_by(sort_field)
            # products - это список двух списков

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        main_category = Category.objects.get(slug=self.kwargs['slug'])
        all_category = Category.objects.filter(parent=None)
        context['category'] = main_category
        context['all_category'] = all_category
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
