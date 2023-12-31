from rest_framework import serializers

from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name')
