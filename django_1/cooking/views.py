from django.shortcuts import render, redirect
from .models import Category, Post
from .forms import PostForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import PostSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# def index(request):
#     posts = Post.objects.filter(is_published=True)
#
#     context = {
#         'title': 'Главная страница',
#         'posts': posts,
#
#     }
#
#     return render(request, 'cooking/index.html', context)


class Index(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

# def category_list(request, pk):
#     posts = Post.objects.filter(category_id=pk, is_published=True)
#
#     context = {
#         'title': posts[0].category.title if posts else 'Нет статей данной категории',
#         'posts': posts,
#
#     }
#
#     return render(request, 'cooking/index.html', context)


class ArticleByCategory(Index):
    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


# def post_detail(request, pk):
#     article = Post.objects.get(pk=pk)
#     article.watched += 1
#     article.save()
#
#     context = {
#         'title': article.title,
#         'post': article
#     }
#
#     return render(request, 'cooking/article_detail.html', context)

class ArticleDetail(DetailView):
    model = Post
    template_name = 'cooking/article_detail.html'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Post.objects.get(pk=self.kwargs['pk'])
        article.watched += 1
        article.save
        context['title'] = f'Статья: {article.title}'
        return context


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()

            return redirect('post_detail', post.pk)
    else:
        form = PostForm()

    contex = {
        'form': form,
        'title': 'Добавить статью'
    }

    return render(request, 'cooking/article_form.html', contex)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('index')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }

    return render(request, 'cooking/login_form.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }

    return render(request, 'cooking/reqister.html', context)




class CookingAPI(ListAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CookingAPIDetail(RetrieveAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CookingCategoryAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CookingCategoryAPIDetail(RetrieveAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = CategorySerializer
