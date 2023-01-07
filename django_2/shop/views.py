from random import randint

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product, Review, FavoriteProducts
from .forms import LoginForm, RegistrationForm, ReviewForm
from django.contrib.auth import login, logout
from django.contrib import messages


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=product.category)
        data = []
        for i in range(4):
            random_index = randint(0, len(products) - 1)
            random_product = products[random_index]
            if random_product not in data and str(random_product) != product.title:
                data.append(random_product)

        context['products'] = data
        context['reviews'] = Review.objects.filter(product=product)
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()

        return context


def login_registration(request):
    context = {
        'title': 'Войти или зарегестрироваться',
        'login_form': LoginForm(),
        'registration_form': RegistrationForm()
    }

    return render(request, 'shop/login_registration.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('product_list')
    else:
        messages.error(request, 'Не верное имя пользователя или пароль')
        return redirect('login_registration')


def user_logout(request):
    logout(request)
    return redirect('product_list')


def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'Аккаунт успешно создан. Войдите в аккаунт')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())

    return redirect('login_registration')


def save_review(request, product_id):
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(pk=product_id)
        review.product = product
        review.save()

    return redirect('product_detail', product.slug)


def save_favorite_product(request, product_slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=product_slug)
    favorite_products = FavoriteProducts.objects.filter(user=user)
    if user:
        if product in [ i.product for i in favorite_products ]:
            fav_product = FavoriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavoriteProducts.objects.create(user=user, product=product)
    next_page = request.META.get('HTTP_REFERER', 'products_list')

    return redirect(next_page)