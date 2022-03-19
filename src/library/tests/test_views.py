from django.test import TestCase
from library.models import *
from django.contrib.auth.models import Permission
import uuid

from library.views import *
from model_bakery import baker


class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        test_book = Book.objects.create(title="How to Test genres",
                                        summary="Book to test genres",
                                        isbn="1234567890124")
        test_book.author.add(test_author)

        test_author2 = Author.objects.create(first_name="Jane", last_name="Milburn")
        test_book2 = Book.objects.create(title="How to put on socks",
                                         summary="Safe use of socks",
                                         isbn="1234567890124")
        test_book2.author.add(test_author2)

        test_author3 = Author.objects.create(first_name="John", last_name="Sax")
        test_book3 = Book.objects.create(title="How to Test genres",
                                         summary="Book to test genres",
                                         isbn="1234567890124")
        test_book3.author.add(test_author3)

        # Test user with permission to view other users
        test_user0 = User.objects.create_user(username='testuser0',
                                              first_name="Admin",
                                              last_name="BOFH",
                                              password='12345')
        permission_view_user = Permission.objects.get(codename='view_member')
        test_user0.user_permissions.add(permission_view_user)

        test_user1 = User.objects.create_user(username='testuser1',
                                              first_name="Max",
                                              last_name="Müller",
                                              password='12345')
        test_user1.save()
        cls.test_user2 = User.objects.create_user(username='testuser2',
                                                  first_name="Mia-Mo Michael",
                                                  last_name="Müller",
                                                  password='12345')
    def test_author_search(self):
        authors = get_authors("Jane")
        books = get_books_of_authors(authors)
        self.assertEqual(2, len(books))

    def test_user_search(self):
        from library.views import get_user
        query = "Müller"
        result = get_user(query)
        self.assertEqual(2, len(result))

        query = "Mia-Mo"
        result = get_user(query)
        self.assertEqual(1, len(result))

        query = "Marvin"
        result = get_user(query)
        self.assertEqual(0, len(result))

        """Allows Max to be present, has to find Mia-Mo"""
        query = "Mia-Mo Michael Müller"
        result = get_user(query)
        self.assertTrue(self.test_user2 in result)

    def test_user_search_view(self):
        """Has to find Mia-Mo and Max"""
        self.client.login(username='testuser0', password='12345')

        response = self.client.post(reverse('library:search'), data={'q': "Müller"})
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser0')
        self.assertTrue((len(response.context['user_list']) > 0))
        self.assertContains(response, "Max")
        self.assertContains(response, "Mia-Mo")

        """Allows Max to be present, has to find Mia-Mo"""
        response = self.client.post(reverse('library:search'), data={'q': "Mia-Mo Michael Müller"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mia-Mo")

        """Has to find Mia-Mo and not Max"""
        response = self.client.post(reverse('library:search'), {'q': "Mia-Mo"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mia-Mo")
        self.assertNotContains(response, "Max")


# Tests the view of library/my-loans/
class MyLoansView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_book = baker.make_recipe("library.book")
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy % 5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            b = BookInstance.objects.create(
                book=test_book,
                label=f'A {book_copy}',
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('library:my-loans'))
        self.assertRedirects(response, '/accounts/login/?next=/library/my-loans/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:my-loans'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/list_loans_user.html')

    # Tests if the borrowed items of the user are really shown, only shown when on loan and not anymore books
    def test_content(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:my-loans'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that initially we don't have any items in list (none on loan)
        self.assertTrue('unreturned_loans' in response.context)
        self.assertTrue('returned_loans' in response.context)
        self.assertEqual(len(response.context['unreturned_loans']) + len(response.context['returned_loans']), 0)

        # Now change all books to be on loan
        books = BookInstance.objects.all()[:10]

        borrower = Member.objects.get(user=User.objects.get(username="testuser1"))
        for book in books:
            book.borrow(borrower=borrower)

        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('library:my-loans'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('unreturned_loans' in response.context)
        self.assertTrue('returned_loans' in response.context)
        # Check that all books are in context
        self.assertEqual(len(response.context['unreturned_loans']), 10)
        # Confirm all books belong to testuser1 and are on loan
        for loan in response.context['unreturned_loans']:
            self.assertEqual(loan.item.status, 'o')


class LoanDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        test_book = baker.make_recipe("library.book")
        # User to borrow the book
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        # User without permission to see borrower
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        # User with permission to see borrower
        test_user3 = User.objects.create_user(username='testuser3', password='12345')
        permission_see = Permission.objects.get(codename="can_see_borrowed")
        test_user3.user_permissions.add(permission_see)
        test_user3.save()

        b = BookInstance.objects.create(
            book=test_book,
            label=f'A 1 a',
            status="a",
        )
        b.borrow(Member.objects.get(user=test_user1))
        b.save()
        cls.loan1 = Loan.objects.filter(item=b)[0]

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:loan-detail', kwargs={'pk': self.loan1.pk}))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/loan-detail.html')

    def test_info_without_login(self):
        response = self.client.get(reverse('library:loan-detail', kwargs={'pk': self.loan1.pk}))
        # Check that we got a response "success" and use correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/loan-detail.html')

        # Check that general loan info but not information on borrower is shown
        self.assertContains(response, f"{self.loan1.pk}")
        self.assertContains(response, str(self.loan1.item.label))
        self.assertNotContains(response, str(self.loan1.borrower))

    def test_info_with_login_no_permission(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('library:loan-detail', kwargs={'pk': self.loan1.pk}))
        # Check that we got a response "success" and use correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/loan-detail.html')

        # Check that general loan info but not information on borrower is shown
        self.assertContains(response, f"{self.loan1.pk}")
        self.assertContains(response, str(self.loan1.item.label))
        self.assertNotContains(response, str(self.loan1.borrower))

    def test_info_with_see_permission(self):
        login = self.client.login(username='testuser3', password='12345')
        response = self.client.get(reverse('library:loan-detail', kwargs={'pk': self.loan1.pk}))
        # Check that we got a response "success" and use correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/loan-detail.html')

        # Check that general loan info and information on borrower is shown
        self.assertContains(response, f"{self.loan1.pk}")
        self.assertContains(response, str(self.loan1.item.label))
        self.assertContains(response, str(self.loan1.borrower))


class AllLoanView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        b = Book.objects.create(title="How to Test",
                                summary="How to write better tests than you do",
                                isbn="1234567890123")
        b.author.add(test_author)
        cls.test_user1 = User.objects.create_user(username='testuser1', password='12345')
        cls.test_user2 = User.objects.create_user(username='testuser2', password='12345')
        permission = Permission.objects.get(name__iexact="See all borrowed items")
        cls.test_user2.user_permissions.add(permission)
        cls.test_user2.save()
        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            status = 'm'
            BookInstance.objects.create(
                book=b,
                label=f'A {book_copy}',
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('library:loans'))
        self.assertRedirects(response, '/accounts/login/?next=/library/loans/')

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:loans'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('library:loans'))
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/list_loans.html')

        # Tests if the borrowed items of the user are really shown, only shown when on loan and not anymore books

    def test_content(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('library:unreturned-loans'))
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')

        # Check that initially we don't have any books in list (none on loan)
        self.assertTrue('loan_list' in response.context)
        self.assertEqual(sum([isinstance(loan.item, BookInstance) for loan in response.context['loan_list']]), 0)

        # Now change some books to be on loan
        books = BookInstance.objects.all()[:20]

        for idx, book in enumerate(books):
            the_borrower = Member.objects.get(user=self.test_user1) if idx % 2 else Member.objects.get(
                user=self.test_user2)
            book.borrow(borrower=the_borrower)

        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('library:unreturned-loans'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('loan_list' in response.context)
        # Check that all books are in context
        self.assertEqual(sum([isinstance(loan.item, BookInstance) for loan in response.context['loan_list']]), 20)
        # Confirm are on loan
        for loan in response.context['loan_list']:
            self.assertEqual(loan.item.status, 'o')

        # Confirm content is displayed
        self.assertContains(response, self.test_user1.username)
        self.assertContains(response, self.test_user2.username)
        self.assertContains(response, "A 1")


class AuthorViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_author1 = Author.objects.create(first_name="Jane", last_name="Doe")
        cls.test_author1.save()
        cls.test_author2 = Author.objects.create(first_name="Jim", last_name="Butch")
        cls.test_author2.save()
        cls.test_book = Book.objects.create(title="How to Test views",
                                            summary="How to write better tests than you do",
                                            isbn="1234567890123")
        cls.test_book.author.add(cls.test_author1)

    def test_use_of_correct_template(self):
        response = self.client.get(self.test_author1.get_absolute_url())
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/author.html')

    def test_book_list(self):
        response = self.client.get(self.test_author1.get_absolute_url())

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that a book by this author is displayed
        self.assertContains(response, "How to Test views")
        self.assertNotContains(response, "No books by this author.")

        response = self.client.get(self.test_author2.get_absolute_url())

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that a author without books is correctly displayed
        self.assertNotContains(response, "How to Test views")
        self.assertContains(response, "No books by this author.")


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/library/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('library:authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('library:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/authors.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('library:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('library:authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)


class BookDetailViewTest(TestCase):
    def setUp(self):
        test_author1 = Author.objects.create(first_name='John', last_name='Smith')
        test_author2 = Author.objects.create(first_name='Jane', last_name='Hammer')
        test_language = Language.objects.create(name='English')
        self.test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            language=test_language,
        )
        self.test_book.author.add(test_author1)
        self.test_book.author.add(test_author2)

    def test_details(self):
        response = self.client.get(reverse('library:book-detail', kwargs={'pk': self.test_book.pk}))
        # Check that site access is permitted
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertContains(response, "Jane Hammer")
        self.assertContains(response, "Smith")
        self.assertContains(response, "Book Title")
        self.assertContains(response, "My book summary")


class BookInstancesDetailViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Give test_user1 permission to see borrower books.
        permission_see = Permission.objects.get(name="See all borrowed items")
        test_user1.user_permissions.add(permission_see)
        test_user1.save()

        # Give test_user2 permission to renew books.
        permission_return = Permission.objects.get(name='Set item as returned')
        test_user2.user_permissions.add(permission_return)
        test_user2.save()

        # Create a book
        test_book = baker.make_recipe("library.book")

        # Create a BookInstance object for test_user1
        self.test_bookinstance1 = baker.make(BookInstance)
        self.test_bookinstance2 = baker.make(BookInstance)

        self.test_bookinstance1.borrow(Member.objects.get(user=test_user1))
        self.test_bookinstance2.borrow(Member.objects.get(user=test_user1))

    def test_logged_in_with_permission_see_borrower(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('library:bookInstance-detail', kwargs={'pk': self.test_bookinstance2.pk}))
        # Check that site access is permitted
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that view contains borrower
        self.assertContains(response, "Borrowed by:")
        self.assertContains(response, "testuser1")

    def test_logged_in_with_permission_to_renew(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('library:bookInstance-detail', kwargs={'pk': self.test_bookinstance2.pk}))

        # Check that user has permission to access site
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')
        # Check that view doesn't contain borrower (user 2 does not have this permission)
        self.assertNotContains(response, "Borrowed by:")
        self.assertContains(response, "Renew")


class MaterialInstancesDetailViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Give test_user1 permission to see borrower books.
        permission_see = Permission.objects.get(name="See all borrowed items")
        test_user1.user_permissions.add(permission_see)
        test_user1.save()

        # Give test_user2 permission to renew books.
        permission_return = Permission.objects.get(name='Set item as returned')
        test_user2.user_permissions.add(permission_return)
        test_user2.save()

        # Create a material
        test_material = Material.objects.create(name="Lab coat")
        test_material.save()

        # Create a MaterialInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_materialinstance1 = MaterialInstance.objects.create(
            material=test_material,
            status='o',
            label="1",
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_materialinstance2 = MaterialInstance.objects.create(
            material=test_material,
            status='o',
            label="2",
        )

    def test_logged_in_with_permission_see_borrower(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('library:materialInstance-detail', kwargs={'pk': self.test_materialinstance2.pk}))
        # Check that site access is permitted
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that view contains borrower
        self.assertContains(response, "Borrowed by:")
        self.assertNotContains(response, "Renew")

    def test_logged_in_with_permission_to_renew(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('library:materialInstance-detail', kwargs={'pk': self.test_materialinstance2.pk}))

        # Check that user has permission to access site
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')
        # Check that view doesn't contain borrower (user 2 does not have this permission)
        self.assertNotContains(response, "Borrowed by:")
        self.assertContains(response, "Renew")


class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        # Give test_user2 permission to renew materials.
        permission = Permission.objects.get(name='Set item as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        test_user3 = User.objects.create_user(username='testuser3', password='12345678')
        # Give test_user3 permission to renew materials and see.
        permission_return = Permission.objects.get(name='Set item as returned')
        permission_see = Permission.objects.get(name="See all borrowed items")
        test_user3.user_permissions.add(permission_return)
        test_user3.user_permissions.add(permission_see)
        test_user3.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = baker.make_recipe("library.book")

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)  # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            status='a',
            label="1",
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            status='a',
            label="2",
        )
        self.test_bookinstance1.borrow(Member.objects.get(user=test_user1))
        self.test_bookinstance2.borrow(Member.objects.get(user=test_user1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('library:renew-item-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('library:renew-item-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('library:renew-item-librarian', kwargs={'pk': self.test_bookinstance2.pk}))

        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('library:renew-item-librarian', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('library:renew-item-librarian', kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('library:renew-item-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/item_renew_librarian.html')

    def test_valid_renew(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('library:renew-item-librarian',
                                            kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': datetime.date.today() + datetime.timedelta(days=20)}
                                    )
        # Successful request should redirect
        self.assertRedirects(response, '/library/')

    def test_invalid_renew(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('library:renew-item-librarian',
                                            kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': datetime.date.today() - datetime.timedelta(days=3)},
                                    )
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')

        # Unsuccessful request should not redirect, but show the form again
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/item_renew_librarian.html')

        # Check response shows error message
        self.assertContains(response, "Invalid date - renewal in past")


class RenewMaterialInstancesViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        # Give test_user2 permission to renew materials.
        permission = Permission.objects.get(name='Set item as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        test_user3 = User.objects.create_user(username='testuser3', password='12345678')
        # Give test_user3 permission to renew materials and see.
        permission_return = Permission.objects.get(name='Set item as returned')
        permission_see = Permission.objects.get(name="See all borrowed items")
        test_user3.user_permissions.add(permission_return)
        test_user3.user_permissions.add(permission_see)
        test_user3.save()

        # Create a material
        test_material = Material.objects.create(
            name='Lab Coat',
        )
        test_material.save()

        # Create a MaterialInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_materialinstance1 = MaterialInstance.objects.create(
            material=test_material,
            status='a',
            label="1",
        )

        # Create a MaterialInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_materialinstance2 = MaterialInstance.objects.create(
            material=test_material,
            status='a',
            label="2",
        )
        self.test_materialinstance1.borrow(Member.objects.get(user=test_user1))
        self.test_materialinstance2.borrow(Member.objects.get(user=test_user1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('library:renew-item-librarian', kwargs={'pk': self.test_materialinstance1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('library:renew-item-librarian', kwargs={'pk': self.test_materialinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_material(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('library:renew-item-librarian', kwargs={'pk': self.test_materialinstance2.pk}))

        # Check that it lets us login - this is our material and we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_material(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('library:renew-item-librarian', kwargs={'pk': self.test_materialinstance1.pk}))

        # Check that it lets us login. We're a librarian, so we can view any users material
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_material_if_logged_in(self):
        # unlikely UID to match our materialinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('library:renew-item-librarian', kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('library:renew-item-librarian', kwargs={'pk': self.test_materialinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/item_renew_librarian.html')

    def test_valid_renew(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('library:renew-item-librarian',
                                            kwargs={'pk': self.test_materialinstance1.pk}),
                                    {'renewal_date': datetime.date.today() + datetime.timedelta(days=20)}
                                    )
        # Successful request should redirect
        self.assertRedirects(response, '/library/')

    def test_invalid_renew(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('library:renew-item-librarian',
                                            kwargs={'pk': self.test_materialinstance1.pk}),
                                    {'renewal_date': datetime.date.today() - datetime.timedelta(days=3)},
                                    )

        # Unsuccessful request should not redirect, but show the form again
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/item_renew_librarian.html')

        # Check response shows error message
        self.assertContains(response, "Invalid date - renewal in past")


"""
Test the view of the index page
"""


class IndexViewTest(TestCase):
    def setUp(self):
        # Create three user
        test_user = baker.make_recipe("library.user", 3)

        # Create authors
        test_author1 = baker.make_recipe("library.author")
        test_author2 = baker.make_recipe("library.author")

        # Create a book
        test_book = baker.make_recipe("library.book", author=[test_author1])
        test_book2 = baker.make_recipe("library.book", author=[test_author1, test_author2])

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance0 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            status='a',
            label="0",
        )

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            status='o',
            label="1",
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            status='o',
            label="2",
        )
        self.test_bookinstance1.borrow(Member.objects.get(user=test_user[0]))
        self.test_bookinstance2.borrow(Member.objects.get(user=test_user[0]))

    # Test if the correct template is used for the library index
    def test_uses_correct_template(self):
        response = self.client.get(reverse('library:index'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/index.html')

        response = self.client.get('/library/')
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/index.html')

    # Test that the site root redirects to the library index
    def test_index_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/library/', status_code=301)

    def test_index_content(self):
        response = self.client.get(reverse('library:index'))

        self.assertEqual(response.status_code, 200)
        # Check that statistics numbers match
        self.assertEqual(response.context['books'], 2)
        self.assertEqual(response.context['book_instances'], 3)
        self.assertEqual(response.context['book_instances_available'], 1)
        self.assertEqual(response.context['authors'], 2)
        self.assertEqual(response.context['users'], 3)


class OpeningHoursCreateViewTest(TestCase):
    """Tests the create view for opening hours"""

    def setUp(self):
        # Normal user
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        # User with permission to create opening hours
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        create_permission = Permission.objects.get(codename='change_opening_hours')
        test_user2.user_permissions.add(create_permission)
        test_user1.save()
        test_user2.save()

    def test_without_login(self):
        response = self.client.get(reverse('library:openinghour-create'))
        self.assertRedirects(response, '/accounts/login/?next=/library/openinghour/create')

    def test_with_login(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:openinghour-create'))
        self.assertEqual(response.status_code, 403)

    def test_with_permission(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('library:openinghour-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/openinghours_form.html")


class BorrowProcedureTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_book = baker.make_recipe("library.book")
        cls.test_user1 = User.objects.create_user(username='testuser1', password='12345')
        cls.test_user2 = User.objects.create_user(username='testuser2', password='12345')
        permission = Permission.objects.get(name__iexact="Can add a loan for all user")
        cls.test_user2.user_permissions.add(permission)
        cls.test_user2.save()
        cls.test_booklinstance1 = BookInstance.objects.create(
            book=test_book,
            label=f'A1 a',
            status="a",
        )

    def test_item_borrow_unauthorized(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:item-borrow', kwargs={'pk': self.test_booklinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_item_borrow_authorized(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('library:item-borrow', kwargs={'pk': self.test_booklinstance1.pk}))
        self.assertEqual(response.status_code, 200)
