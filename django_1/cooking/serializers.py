from rest_framework import serializers

from .models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        """dsfsd"""
        model = Post
        fields = ('title', 'id', 'category', 'created_at', 'content')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'id')
