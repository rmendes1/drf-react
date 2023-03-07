from django.test import TestCase
from django.urls import reverse 
from rest_framework import status
from rest_framework.test import APITestCase 
from blog.models import Post, Category 
from django.contrib.auth.models import User 
from rest_framework.test import APIClient

class PostTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='django')
        self.user1 = User.objects.create_user(username='testuser1', password='1234567')
        self.user2 = User.objects.create_user(username='testuser2', password='12345678')
        self.post = Post.objects.create(
            category=self.category,
            title='Post Title',
            excerpt='Excerpt 1',
            content='Content 1',
            author=self.user1,
            status='published',
        )

    def test_view_posts(self):
        """Tests if a user can see the posts list"""
        self.client.force_login(self.user1)
        url = reverse('blogapi:listcreate')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    
    def create_post(self):
        """Tests if a user can create a post"""
        self.client.force_login(self.user1)
        url = reverse('blogapi:listcreate')
        data = {
            "title": "New",
            "author": 1,
            "excerpt": "New",
            "content": "New",
            "category": self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_update(self):
        """Tests if a different user can edit a post from another author"""

        url = reverse('blogapi:detailcreate', kwargs={"pk": self.post.id})
        
        # testing user1
        self.client.force_login(self.user1)
        data = {
            "title": "New",
            "author": self.user1.id,
            "excerpt": "New",
            "content": "New",
            "category": self.category.id,
            "status": "published"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # testing user2
        self.client.force_login(self.user2)
        data = {
            "title": "New",
            "author": self.user1.id,
            "excerpt": "New",
            "content": "New",
            "category": self.category.id,
            "status": "published"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
