from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date
from django.utils.translation import ugettext_lazy as _


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Material(models.Model):
    def __str__(self):
        return f"{self.name}"
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('library:material-detail', args=[str(self.id)])
    name = models.CharField(max_length=200)

class Book(models.Model):
    def __str__(self):
        return f"{self.title} by {self.author}"
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('library:book-detail', args=[str(self.id)])

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='ISBN number (13 Characters)')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)


class Item(models.Model):
    """Represents an item that is physically in the library"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular item across whole library')
    label = models.CharField(max_length=20, unique=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Item availability',
    )

    class Meta:
        permissions = (("can_mark_returned", "Set item as returned"),
                       ("can_see_borrowed", "See all borrowed items"))


class BookInstance(Item):
    """Represents a copy of a book that is physically in the library"""
    def __str__(self):
        return f"[{self.label}] {self.book.title} by {self.book.author}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this bookInstance."""
        return reverse('library:bookInstance-detail', args=[str(self.id)])

    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200, null=True, blank=True)

class MaterialInstance(Item):
    """Represents a instance of a material that is physically in the library"""

    def __str__(self):
        return f"[{self.label}] {self.material.name}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this materialInstance."""
        return reverse('library:materialInstance-detail', args=[str(self.id)])

    material = models.ForeignKey('Material', on_delete=models.RESTRICT, null=True)

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_modify_author", "Can add, update or delete an author"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('library:author-detail', args=[str(self.id)])

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Loan(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    lent_on = models.DateField()
    due_back = models.DateField()
    returned_on = models.DateField(null=True, blank=True)

    def __str__(self):
        """String representation."""
        return f"{self.item} borrowed by {self.borrower}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this loan."""
        return reverse('library:loan-detail', args=[str(self.id)])

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    @property
    def returned(self):
        return self.returned_on

WEEKDAYS = [
  (1, _("Monday")),
  (2, _("Tuesday")),
  (3, _("Wednesday")),
  (4, _("Thursday")),
  (5, _("Friday")),
  (6, _("Saturday")),
  (7, _("Sunday")),
]

class OpeningHours(models.Model):

    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    comment = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')
        permissions = (('change_opening_hours', 'Can change opening hours'),)

    def __str__(self):
        return f"{self.get_weekday_display()} {self.from_hour:%H:%M}-{self.to_hour:%H:%M}"