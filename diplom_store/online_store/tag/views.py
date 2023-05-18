from rest_framework.response import Response
from rest_framework.views import APIView

from tag.models import Tag
from tag.serializers import TagSerializer

class TagsView(APIView):
    """
    Представление для получения тегов.
    """
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)