from django.db import models

class Book(models.Model):
    def __str__(self):
        return f"{self.title} by {self.author}"
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    aquired_date = models.DateTimeField('date aquired')

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    lent_on = models.DateTimeField('date lent')
    returned_on = models.DateTimeField('date returned')

