from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date


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

class MaterialInstance(models.Model):
        """Represents a instance of a material that is physically in the library"""

        def __str__(self):
            return f"[{self.label}] {self.material.name}"

        def get_absolute_url(self):
            """Returns the url to access a detail record for this materialInstance."""
            return reverse('library:materialInstance-detail', args=[str(self.id)])

        @property
        def is_overdue(self):
            if self.due_back and date.today() > self.due_back:
                return True
            return False

        id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                              help_text='Unique ID for this particular book across whole library')
        material = models.ForeignKey('Material', on_delete=models.RESTRICT, null=True)
        label = models.CharField(max_length=20, unique=True)
        due_back = models.DateField(null=True, blank=True)
        borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
            help_text='Material availability',
        )

        class Meta:
            permissions = (("can_mark_returned", "Set material as returned"),
                           ("can_see_borrowed", "See all borrowed material&borrower"))

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

class BookInstance(models.Model):
    """Represents a copy of a book that is physically in the library"""
    def __str__(self):
        return f"[{self.label}] {self.book.title} by {self.book.author}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this bookInstance."""
        return reverse('library:bookInstance-detail', args=[str(self.id)])

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    label = models.CharField(max_length=20, unique=True)
    imprint = models.CharField(max_length=200, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
        help_text='Book availability',
    )

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),
                       ("can_see_borrowed", "See all borrowed books"))

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