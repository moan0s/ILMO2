from django.test import TestCase
from library.models import *
from library.templatetags.custom_tags import is_materialinstance, is_bookinstance


class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        test_book = Book.objects.create(title="Whatever",
                                        isbn="1234567890124")
        test_book.author.add(test_author)
        cls.bookinstance = BookInstance.objects.create(label="B1 a",
                                                       book=test_book)

        test_material = Material.objects.create(name="Kryptonite Block")
        cls.materialinstance = MaterialInstance.objects.create(label="M1 a",
                                                               material=test_material)

    def test_is_materialinstance(self):
        self.assertTrue(is_materialinstance(self.materialinstance))
        self.assertFalse(is_materialinstance(self.bookinstance))

    def test_is_bookinstance(self):
        self.assertFalse(is_bookinstance(self.materialinstance))
        self.assertTrue(is_bookinstance(self.bookinstance))
