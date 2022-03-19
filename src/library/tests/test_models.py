from django.test import TestCase

from library.models import *
from datetime import timedelta, time
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        a1 = Author.objects.create(first_name="Jane", last_name="Doe")
        a2 = Author.objects.create(first_name="Jane", last_name="Günter")
        a1.save()
        a2.save()

    def test_object_name_is_normalized(self):
        author = Author.objects.all()[0]
        expected_object_name = f"{author.first_name} {author.last_name}"
        self.assertEquals(str(author), expected_object_name)

    def test_special_character(self):
        author = Author.objects.all()[1]
        self.assertEquals(author.last_name, "Günter")

    def test_date_birth_optional(self):
        author = Author.objects.all()[0]
        plank_property = author._meta.get_field('date_of_birth').blank
        self.assertEquals(plank_property, True)

    def test_date_death_optional(self):
        author = Author.objects.all()[0]
        plank_property = author._meta.get_field('date_of_death').blank
        self.assertEquals(plank_property, True)

    def test_ordering(self):
        author = Author.objects.all()[0]
        ordering = author._meta.ordering
        self.assertEquals(ordering, ['last_name', 'first_name'])

    def test_first_name_label(self):
        author = Author.objects.all()[0]
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'First name')

    def test_date_of_death_label(self):
        author = Author.objects.all()[0]
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Date of death')

    def test_first_name_max_length(self):
        author = Author.objects.all()[0]
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_get_absolute_url(self):
        author = Author.objects.all()[0]
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), f'/library/author/{author.id}/')


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(ctl):
        g1 = Genre.objects.create(name="Science Fiction")
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        b1 = Book.objects.create(title="How to Test",
                                 summary="How to write better tests than you do",
                                 isbn="1234567890123")
        b1.author.add(test_author)
        g1.save()
        b1.save()

    def test_str(self):
        genre = Genre.objects.all()[0]
        string_representation = str(genre)
        self.assertEquals(string_representation, f"Science Fiction")

    def add_genre_to_book(self):
        book = Book.objects.all()[0]
        genre = Genre.objects.all()[0]
        book.genre.set(genre)
        string_representation = str(book.genre)
        self.assertEquals(string_representation, f"Science Fiction")


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        b = Book.objects.create(title="How to Test",
                                summary="How to write better tests than you do",
                                isbn="1234567890123")
        test_author.save()
        b.save()
        b.author.add(test_author)
        b.save()
        print("")

    def test_str(self):
        book = Book.objects.all()[0]
        string_representation = str(book)
        self.assertEquals(f"How to Test by Jane Doe",
                          string_representation)


class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        test_author.save()
        b = Book.objects.create(title="How to Test",
                                summary="How to write better tests than you do",
                                isbn="1234567890123")
        b.author.add(test_author)
        bookInstanceA = BookInstance.objects.create(book=b, label="T 1 a")
        b.save()
        bookInstanceA.save()

        u = User.objects.create_user('foo', password='bar')
        bookInstanceB = BookInstance.objects.create(book=b,
                                                    label="T 1 b", )

        bookInstanceC = BookInstance.objects.create(book=b,
                                                    label="T 1 c", )
        bookInstanceB.save()
        bookInstanceC.save()

    def test_str(self):
        bookInstance = BookInstance.objects.filter(label="T 1 a")[0]
        string_representation = str(bookInstance)
        self.assertEquals(string_representation, f"[T 1 a] How to Test by Jane Doe")

    def test_default(self):
        bookInstance = BookInstance.objects.all()[0]
        self.assertEquals(bookInstance.status, "m")

    def test_get_absolute_url(self):
        bookInstanceB = BookInstance.objects.filter(label="T 1 b")[0]
        self.assertEquals(f"/library/bookInstance/{bookInstanceB.id}",
                          bookInstanceB.get_absolute_url())


class MaterialModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        a1 = Material.objects.create(name="Lab Coat")
        a1.save()

    def test_name_max_length(self):
        material = Material.objects.all()[0]
        max_length = material._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_material_str_representation(self):
        material = Material.objects.all()[0]
        expected_object_name = f'{material.name}'
        self.assertEqual(str(material), expected_object_name)

    def test_get_absolute_url(self):
        material = Material.objects.all()[0]
        # This will also fail if the urlconf is not defined.
        self.assertEqual(material.get_absolute_url(), f'/library/material/{material.id}')


class MaterialInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        m = Material.objects.create(name="Lab Coat")
        materialInstanceA = MaterialInstance.objects.create(material=m, label="LC 1")
        m.save()
        materialInstanceA.save()

        materialInstanceB = MaterialInstance.objects.create(material=m,
                                                            label="LC 2", )

        materialInstanceC = MaterialInstance.objects.create(material=m,
                                                            label="LC 3", )
        materialInstanceB.save()
        materialInstanceC.save()

    def test_str(self):
        materialInstance = MaterialInstance.objects.filter(label="LC 1")[0]
        string_representation = str(materialInstance)
        self.assertEquals(string_representation, f"[LC 1] {materialInstance.material.name}")

    def test_default(self):
        materialInstance = MaterialInstance.objects.all()[0]
        self.assertEquals(materialInstance.status, "m")

    def test_get_absolute_url(self):
        materialInstanceB = MaterialInstance.objects.filter(label="LC 3")[0]
        self.assertEquals(f"/library/materialInstance/{materialInstanceB.id}",
                          materialInstanceB.get_absolute_url())


class ItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        b = Book.objects.create(title="How to Test",
                                summary="How to write better tests than you do",
                                isbn="1234567890123")
        b.author.add(test_author)
        cls.bookInstanceA = BookInstance.objects.create(book=b, label="T 1 a")
        cls.u = User.objects.create_user('foo', password='bar')
        cls.u.save()

    def test_borrow(self):
        self.bookInstanceA.borrow(Member.objects.get(user=self.u))
        self.assertEquals(self.bookInstanceA.status, "o")
        loans_of_book = Loan.objects.filter(item=self.bookInstanceA)
        self.assertEquals(len(loans_of_book), 1)
        loan = loans_of_book[0]
        self.assertFalse(loan.returned)
        self.assertFalse(loan.is_overdue)
        self.assertEquals(loan.borrower, Member.objects.get(user=self.u))

        # Test default return
        self.assertEquals(loan.due_back, (timezone.now() + timedelta(days=28)).date())

    def test_return(self):
        self.bookInstanceA.borrow(Member.objects.get(user=self.u))
        self.assertEquals(self.bookInstanceA.status, "o")
        loans_of_book = Loan.objects.filter(item=self.bookInstanceA)
        self.assertEquals(len(loans_of_book), 1)
        loan = loans_of_book[0]
        self.assertFalse(loan.returned)
        self.assertFalse(loan.is_overdue)
        self.assertEquals(loan.borrower, Member.objects.get(user=self.u))

        # Return item and check expected state
        self.assertTrue(self.bookInstanceA.return_item())
        # Reload the loan
        loans_of_book = Loan.objects.filter(item=self.bookInstanceA)
        self.assertEquals(len(loans_of_book), 1)
        loan = loans_of_book[0]
        self.assertTrue(loan.returned)
        self.assertFalse(loan.is_overdue)
        self.assertEquals(self.bookInstanceA.status, "a")


class LoanModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        b = Book.objects.create(title="How to Test",
                                summary="How to write better tests than you do",
                                isbn="1234567890123")
        b.author.add(test_author)
        cls.bookInstanceA = BookInstance.objects.create(book=b, label="T 1 a")
        b.save()
        cls.bookInstanceA.save()

        u = User.objects.create_user('foo', password='bar')
        u.save()
        cls.m1 = Member.objects.get(user=u)
        cls.bookInstanceA.borrow(cls.m1)

    def test_str(self):
        loan = Loan.objects.filter(item=self.bookInstanceA)[0]
        string_representation = str(loan)
        self.assertEquals(string_representation, f"{loan.item} borrowed until {loan.due_back}")

    def test_default(self):
        bookInstance = Loan.objects.all()[0]
        self.assertTrue(bookInstance.returned_on is None)

    def test_get_absolute_url(self):
        loan = Loan.objects.filter(item=self.bookInstanceA)[0]
        self.assertEquals(loan.get_absolute_url(),
                          f"/library/loan/{loan.id}/")

    def test_status(self):
        self.assertEquals("o", self.bookInstanceA.status)
        self.bookInstanceA.return_item()
        self.assertEquals("a", self.bookInstanceA.status)

    def test_borrower(self):
        self.bookInstanceA.borrow(self.m1)
        self.assertEquals(self.m1, self.bookInstanceA.borrower)
        self.bookInstanceA.return_item()
        self.assertEquals("a", self.bookInstanceA.status)
        self.assertEquals(_("Not borrowed"), self.bookInstanceA.borrower)

    def test_num_reminder(self):
        loan = self.bookInstanceA.borrow(self.m1)
        num_reminders_expected = 3
        for i in range(0, num_reminders_expected):
            loan.remind()
        self.assertEquals(loan.num_reminders, num_reminders_expected)


class OpeningHourModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.oh1 = OpeningHours.objects.create(weekday=1,
                                              from_hour=time(hour=12, minute=30),
                                              to_hour=time(hour=13, minute=30), )
        cls.oh1.save()

    def test_string_representation(self):
        self.assertEquals("Monday 12:30-13:30", str(self.oh1))


class MemberModelTest(TestCase):
    def test_auto_creation_of_member(self):
        u = User.objects.create_user('foo', password='bar')
        u.save()
        self.assertEquals(len(Member.objects.filter(user=u)), 1)
