from django.shortcuts import render
from .models import Category, Post


def index(request):
    posts = Post.objects.all()

    context = {
        'title': 'Главная страница',
        'posts': posts,

    }

    return render(request, 'cooking/index.html', context)


def category_list(request, pk):
    posts = Post.objects.filter(category_id=pk)

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
