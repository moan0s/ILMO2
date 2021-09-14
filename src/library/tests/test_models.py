from django.test import TestCase

from library.models import *

class AuthorModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="Jane", last_name="Doe")
        Author.objects.create(first_name="Jane", last_name="Günter")

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(author.last_name, author.first_name)
        self.assertEquals(str(author), expected_object_name)

    def test_special_character(self):
        author = Author.objects.get(id=2)
        self.assertEquals(author.last_name, "Günter")

    def test_date_birth_optional(self):
        author = Author.objects.get(id=1)
        plank_property = author._meta.get_field('date_of_birth').blank
        self.assertEquals(plank_property, True)

    def test_date_death_optional(self):
        author = Author.objects.get(id=1)
        plank_property = author._meta.get_field('date_of_death').blank
        self.assertEquals(plank_property, True)

    def test_ordering(self):
        author = Author.objects.get(id=1)
        ordering = author._meta.ordering
        self.assertEquals(ordering, ['last_name', 'first_name'] )

class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(ctl):
        Genre.objects.create(name="Science Fiction")
        Book.objects.create(title="How to Test genres",
                author=Author.objects.create(first_name="Jane", last_name="Doe"),
                summary="Book to test genres",
                isbn="1234567890124")

    def test_str(self):
        genre = Genre.objects.get(id=1)
        string_representation = str(genre)
        self.assertEquals(string_representation, f"Science Fiction")

    def add_genre_to_book(self):
        book = Book.objects.get(id=1)
        genre = Genre.objects.get(id=1)
        book.genre.set(genre)
        string_representation = str(book.genre)
        self.assertEquals(string_representation, f"Science Fiction")





class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title="How to Test",
                author=Author.objects.create(first_name="Jane", last_name="Doe"),
                summary="How to write better tests than you do",
                isbn="1234567890123")

    def test_str(self):
        book = Book.objects.get(id=1)
        string_representation = str(book)
        self.assertEquals(string_representation, f"How to Test by {book.author}")
