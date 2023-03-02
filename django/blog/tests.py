from django.test import TestCase
from django.contrib.auth.models import User 
from django.utils import timezone
from blog.models import Post, Category 


class PostModelTest(TestCase):

    @classmethod 
    def setUpTestData(cls):
        testcategory = Category.objects.create(name='django')
        testauthor = User.objects.create_user(username='testuser', password='testpass')
        Post.objects.create(
            category_id=1,
            title='Test Title',
            excerpt='Test Excerpt',
            content='Test Content',
            slug='test-title',
            published=timezone.now(),
            author_id=1,
            status='published'
        )
