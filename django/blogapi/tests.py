from django.test import TestCase
from django.urls import reverse 
from rest_framework import status
from rest_framework.test import APITestCase 
from blog.models import Post, Category 
from django.contrib.auth.models import User 
from rest_framework.test import APIClient

class PostTests(APITestCase):

    def test_view_posts(self):
        """Tests if a user can see the posts list"""
        client = APIClient()
        self.testuser1 = User.objects.create_user(username='testuser1', password='1234567')
        client.login(username=self.testuser1.username, password='1234567')
        url = reverse('blogapi:listcreate')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    
    def create_post(self):
        self.test_category = Category.objects.create(name='django')
        self.testuser = User.objects.create_user(username='testuser', password='testpass')

        data = {"title": "new",
                "author": 1,
                "excerpt": "new",
                "content": "new"
                }

        url = reverse('blogapi:listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_update(self):
        """Tests if a different user can edit a post from another author"""
        client = APIClient()

        self.test_category = Category.objects.create(name='django')
        self.testuser1 = User.objects.create_user(username='testuser1', password='1234567') # this is going to be the post author
        self.testuser2 = User.objects.create_user(username='testuser2', password='12345678') # this is to test if this user can change the post

        Post.objects.create(
            category_id=1,
            title='Post Title',
            excerpt='Excerpt 1',
            content='Content 1',
            author_id=1,
            status='published',
        )

        # testing user1
        client.login(username=self.testuser1.username, password='1234567')

        url = reverse(('blogapi:detailcreate'), kwargs={"pk": 1})

        response = client.put(
            url, {
                "id": 1,
                "title": "New",
                "author": 1,
                "excerpt": "New",
                "content": "New",
                "status": "published"
            }, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # testing user2
        client.login(username=self.testuser2.username, password='12345678')

        response = client.put(
            url, {
                "id": 1,
                "title": "New",
                "author": 1,
                "excerpt": "New",
                "content": "New",
                "status": "published"
            }, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
