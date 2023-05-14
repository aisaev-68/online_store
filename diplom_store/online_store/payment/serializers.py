from . import models
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Автор"""
    class Meta:
        model = models.Author
        fields = ('id', 'first_name', 'last_name', 'year_birth')


class StringListSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Книга"""
    authors_names = StringListSerializer()
    class Meta:
        model = models.Book
        fields = ('id', 'title', 'isbn', 'publication_date', 'pages', 'authors', 'authors_names',)
