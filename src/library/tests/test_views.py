from django.test import Client
from django.test import TestCase
from django.urls import reverse
from library.models import *
from django.utils import timezone
import datetime

class MyBooksView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        test_book = Book.objects.create(title="How to Test genres",
                author=Author.objects.create(first_name="Jane", last_name="Doe"),
                summary="Book to test genres",
                isbn="1234567890124")
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                label=f'A {book_copy}',
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('library:my-books'))
        self.assertRedirects(response, '/accounts/login/?next=/library/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        print(login)
        response = self.client.get(reverse('library:my-books'))
        print("Dada")
        print(response)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/bookinstance_list_borrowed_user.html')
    
