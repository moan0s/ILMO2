from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.all().count()

    # Available books
    num_instances_available = BookInstance.objects.filter(status = "a").count()

    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'library/index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    template_name = 'library/books.html'
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'library/book.html'

def loans_of_book(request, pk):
    response = "You're looking at the loans of book %s."
    return HttpResponse(response % pk)

def lend_book(request, pk):
    return HttpResponse("You're lending book %s." % pk)

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'library/author.html'
    paginate_by = 10
    
    from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='library/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')