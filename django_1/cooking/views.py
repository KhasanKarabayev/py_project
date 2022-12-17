from django.shortcuts import render
from .models import Category, Post

from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import PostSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response


def index(request):
    posts = Post.objects.filter(is_published=True)

    context = {
        'title': 'Главная страница',
        'posts': posts,

    }

    return render(request, 'cooking/index.html', context)


def category_list(request, pk):
    posts = Post.objects.filter(category_id=pk, is_published=True)

    context = {
        'title': posts[0].category.title if posts else 'Нет статей данной категории',
        'posts': posts,

    }

    return render(request, 'cooking/index.html', context)


def post_detail(request, pk):
    article = Post.objects.get(pk=pk)
    article.watched += 1
    article.save()

    context = {
        'title': article.title,
        'post': article
    }

    return render(request, 'cooking/article_detail.html', context)


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
