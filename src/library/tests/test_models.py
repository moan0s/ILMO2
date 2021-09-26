from django.test import TestCase

from library.models import *
from datetime import timedelta

class AuthorModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        a1 = Author.objects.create(first_name="Jane", last_name="Doe")
        a2 = Author.objects.create(first_name="Jane", last_name="Günter")
        a1.save()
        a2.save()

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.all()[0]
        expected_object_name = '{0}, {1}'.format(author.last_name, author.first_name)
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
        self.assertEquals(ordering, ['last_name', 'first_name'] )
    def test_first_name_label(self):
        author = Author.objects.all()[0]
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.all()[0]
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.all()[0]
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.all()[0]
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.all()[0]
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), f'/library/author/{author.id}/')

class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(ctl):
        g1 = Genre.objects.create(name="Science Fiction")
        b1 = Book.objects.create(title="How to Test genres",
                author=Author.objects.create(first_name="Jane", last_name="Doe"),
                summary="Book to test genres",
                isbn="1234567890124")
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
        b = Book.objects.create(title="How to Test",
                author=Author.objects.create(first_name="Jane", last_name="Doe"),
                summary="How to write better tests than you do",
                isbn="1234567890123")
        b.save()

    def test_str(self):
        book = Book.objects.all()[0]
        string_representation = str(book)
        self.assertEquals(string_representation, f"How to Test by {book.author}")

class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        b = Book.objects.create(title="How to Test",
                author=Author.objects.create(first_name="Jane", last_name="Doe"),
                summary="How to write better tests than you do",
                isbn="1234567890123")
        bookInstanceA = BookInstance.objects.create(book = b, label = "T 1 a")
        b.save()
        bookInstanceA.save()
        
        u = User.objects.create_user('foo', password='bar')
        bookInstanceB = BookInstance.objects.create(book = b,
            label = "T 1 b",
            borrower = u,
            due_back = date.today() - timedelta(days=1))

        bookInstanceC = BookInstance.objects.create(book = b,
            label = "T 1 c",
            borrower = u,
            due_back = date.today() + timedelta(days=1))
        bookInstanceB.save()
        bookInstanceC.save()

    def test_str(self):
        bookInstance = BookInstance.objects.filter(label="T 1 a")[0]
        string_representation = str(bookInstance)
        self.assertEquals(string_representation, f"[T 1 a] {bookInstance.book.title} by {bookInstance.book.author}")

    def test_default(self):
        bookInstance = BookInstance.objects.all()[0]
        self.assertEquals(bookInstance.status, "m")
    
    def test_due_date(self):
        bookInstanceB = BookInstance.objects.filter(label="T 1 b")[0]
        self.assertEquals(True, bookInstanceB.is_overdue)
        bookInstanceC = BookInstance.objects.filter(label="T 1 c")[0]
        self.assertEquals(False, bookInstanceC.is_overdue)


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

        u = User.objects.create_user('foo', password='bar')
        materialInstanceB = MaterialInstance.objects.create(material=m,
                                                    label="LC 2",
                                                    borrower=u,
                                                    due_back=date.today() - timedelta(days=1))

        materialInstanceC = MaterialInstance.objects.create(material=m,
                                                    label="LC 3",
                                                    borrower=u,
                                                    due_back=date.today() + timedelta(days=1))
        materialInstanceB.save()
        materialInstanceC.save()

    def test_str(self):
        materialInstance = MaterialInstance.objects.filter(label="LC 1")[0]
        string_representation = str(materialInstance)
        self.assertEquals(string_representation, f"[LC 1] {materialInstance.material.name}")

    def test_default(self):
        materialInstance = MaterialInstance.objects.all()[0]
        self.assertEquals(materialInstance.status, "m")

    def test_due_date(self):
        materialInstance2 = MaterialInstance.objects.filter(label="LC 2")[0]
        self.assertEquals(True, materialInstance2.is_overdue)
        materialInstance3 = MaterialInstance.objects.filter(label="LC 3")[0]
        self.assertEquals(False, materialInstance3.is_overdue)
