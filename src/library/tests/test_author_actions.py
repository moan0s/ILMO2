from django.test import TestCase
from library.models import Author, Book, User
from django.urls import reverse

class AuthorTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        test_book = Book.objects.create(title="How to Test genres",
                author=Author.objects.create(first_name="Jane", last_name="Doe"),
                summary="Book to test genres",
                isbn="1234567890124")
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user2 = User.objects.create_user(username='testuser2', password='12345')

    def test_create_author_if_not_logged_in(self):
        response = self.client.get(reverse('library:author-create'))
        
        # Check that there is a correct redirect to the login page
        self.assertRedirects(response, '/accounts/login/?next=/library/author/create/')
        