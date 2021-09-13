from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book

def index(request):
    book_list = Book.objects.order_by('author')[:5]
    context = {'book_list': book_list}
    return render(request, 'library/books.html', context)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'library/book.html', {'book': book})

def loans_of_book(request, book_id):
    response = "You're looking at the loans of book %s."
    return HttpResponse(response % book_id)

def lend_book(request, book_id):
    return HttpResponse("You're lending book %s." % book_id)

