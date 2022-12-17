from rest_framework import serializers

from .models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'id', 'category_id', 'created_at', 'content')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'id')
