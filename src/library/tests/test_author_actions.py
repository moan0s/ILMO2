from django.test import TestCase
from library.models import Author, Book, User
from django.urls import reverse
from django.contrib.auth.models import Permission
from library.helpers import get_author_from_string


class HelperTests(TestCase):
    def test_author_from_string(self):
        authors1 = get_author_from_string("John Cena, Marie Master")
        authors1_firstname = [author.first_name for author in authors1]
        self.assertEqual(len(authors1), 2)
        self.assertTrue("Marie" in authors1_firstname)


class AuthorTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        test_book = Book.objects.create(title="How to Test genres",
                                        summary="Book to test genres",
                                        isbn="1234567890124")
        test_book.author.add(test_author)
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        permission = Permission.objects.get(name="Can add, update or delete an author")
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_create_author_if_not_logged_in(self):
        response = self.client.get(reverse('library:author-create'))

        # Check that there is a correct redirect to the login page
        self.assertRedirects(response, '/accounts/login/?next=/library/author/create/')

    def test_forbidden_if_logged_in_but_no_permission(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:author-create'))

        # Check that there is a a response with HTTP status code 403
        self.assertEqual(response.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('library:author-create'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/author_form.html')

    def test_author_creation(self):
        login = self.client.login(username='testuser2', password='12345')
        num_authors = Author.objects.count()
        response = self.client.post(reverse('library:author-create'),
                                    {'first_name': 'Author',
                                     'last_name': 'Test'})

        # Check that there is a correct redirect to the detail page of the author
        self.assertRedirects(response, f'/library/author/{num_authors + 1}/')