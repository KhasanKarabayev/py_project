from random import randint

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product, Review, FavoriteProducts, Mail
from .forms import LoginForm, RegistrationForm, ReviewForm, ShippingForm, CustomerForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


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

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data()

        if self.request.user.is_authenticated:
            counter_fav = len(FavoriteProducts.objects.filter(user=user))
            context['cnt_fav'] = counter_fav

        return context


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
        user = self.request.user
        all_category = Category.objects.filter(parent=None)
        context['category'] = main_category
        context['all_category'] = all_category

        if self.request.user.is_authenticated:
            counter_fav = len(FavoriteProducts.objects.filter(user=user))
            context['cnt_fav'] = counter_fav

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
        user = self.request.user
        if self.request.user.is_authenticated:
            counter_fav = len(FavoriteProducts.objects.filter(user=user))
            context['cnt_fav'] = counter_fav
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


class FavoriteProductsView(LoginRequiredMixin, ListView):
    extra_context = {
        'title': 'Избранные'
    }
    model = FavoriteProducts
    context_object_name = 'products'
    template_name = 'shop/favorite_products.html'
    login_url = 'login_registration'

    def get_queryset(self):
        user = self.request.user
        favs = FavoriteProducts.objects.filter(user=user)
        products = [i.product for i in favs]
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user = self.request.user

        if self.request.user.is_authenticated:
            counter_fav = len(FavoriteProducts.objects.filter(user=user))
            context['cnt_fav'] = counter_fav

        return context


def save_email(request):
    email = request.POST.get('email')
    user = request.user if request.user.is_authenticated else None
    if email:
        Mail.objects.create(mail=email, user=user)
    next_page = request.META.get('HTTP_REFERER', 'product_list')
    return redirect(next_page)


def send_mail_to_customers(request):
    from conf import settings
    from django.core.mail import send_mail
    if request.method == 'POST':
        test = request.POST.get('text')
        mail_list = Mail.objects.all()
        for email in mail_list:
            mail = send_mail(
                subject='У нас новая акция',
                message=test,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
            print(f'Отправлено ли сообщение на почту {email}? - {bool(mail)}')
    else:
        pass
    return render(request, 'shop/send_mail.html')


def cart(request):
    return render(request, 'shop/cart.html')


def to_cart(request, product_id, action):
    return redirect('cart')


def checkout(request):
    context = {
        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm(),
        'title': 'Оформление заказа'
    }
    return render(request, 'shop/checkout.html', context)