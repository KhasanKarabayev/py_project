from django.shortcuts import render
from .models import Category, Post

def index(request):
    posts = Post.objects.all()
    categories = Category.objects.all()


    context = {
        'title': 'Главная страница',
        'posts': posts,
        'categories': categories
    }

    return render(request, 'cooking/index.html', context)


