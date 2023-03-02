from django.test import TestCase
from django.contrib.auth.models import User 
from django.utils import timezone
from blog.models import Post, Category 
from django.core.exceptions import ValidationError


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

    def test_blog_content(self):
        post = Post.postobjects.get(id=1)
        cat = Category.objects.get(id=1)
        author = f'{post.author}'
        excerpt = f'{post.excerpt}'
        title = f'{post.title}'
        content = f'{post.content}'
        status = f'{post.status}'
        self.assertEqual(author, 'testuser')
        self.assertEqual(title, 'Test Title')
        self.assertEqual(content, 'Test Content')
        self.assertEqual(status, 'published')
        self.assertEqual(str(post), 'Test Title') # test model __str__
        self.assertEqual(str(cat), 'django')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 250)

    def test_status_choices(self):
        post = Post.objects.get(id=1)
        invalid_status = 'invalid'
        post.status = invalid_status
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_postobjects_manager(self):
        post1 = Post.objects.get(id=1)
        post2 = Post.objects.create(
            title='Draft Post',
            excerpt='Draft excerpt',
            content='Draft content',
            slug='draft-post',
            author=post1.author,
            category=post1.category,
            status='draft',
        )
        published_posts = Post.postobjects.all()
        self.assertIn(post1, published_posts)
        self.assertNotIn(post2, published_posts)
