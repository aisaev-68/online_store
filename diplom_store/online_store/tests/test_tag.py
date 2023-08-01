from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tag.models import Tag
from tag.serializers import TagSerializer


class TestTagsView(APITestCase):

    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.tag3 = Tag.objects.create(name='tag3')

    def test_get_tags(self):
        # Test getting all tags
        url = reverse('tags-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Ensure all tags are returned
        self.assertEqual(
            set(response.data),
            set(TagSerializer([self.tag1, self.tag2, self.tag3], many=True).data),
        )