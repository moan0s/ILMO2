from django.db import models


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Book(models.Model):
    def __str__(self):
        return f"{self.title} by {self.author}"
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, default=0, help_text='ISBN number (13 Characters)')

class BookInstance(models.Model):
    """Represents a copy of a book that is physically in the library"""
    def __str__(self):
        return f"[{self.label}] {self.book.title} by {self.book.author}"
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    label = models.CharField(max_length=20)
    available = models.BooleanField(default=True)

class Loan(models.Model):
    book = models.ForeignKey(BookInstance, on_delete=models.RESTRICT)
    lent_on = models.DateTimeField('date lent')
    returned_on = models.DateTimeField('date returned')

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

