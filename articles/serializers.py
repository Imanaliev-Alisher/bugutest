from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):

    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author_email', 'is_public']
        read_only_fields = ['created_at', 'updated_at']
