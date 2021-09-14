from django.test import TestCase

from library.models import Author

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
        print (plank_property)
        self.assertEquals(plank_property, True)
    def test_date_death_optional(self):
        author = Author.objects.get(id=1)
        plank_property = author._meta.get_field('date_of_death').blank
        print (plank_property)
        self.assertEquals(plank_property, True)
    def test_ordering(self):
        author = Author.objects.get(id=1)
        ordering = author._meta.ordering
        self.assertEquals(ordering, ['last_name', 'first_name'] )
