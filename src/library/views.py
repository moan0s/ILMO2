from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
import datetime

from .forms import RenewBookForm, RenewMaterialForm
from .models import Book, Author, BookInstance, Genre, Material, MaterialInstance, OpeningHours

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
    paginate_by =10

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'library/book.html'

#TODO
def loans_of_book(request, pk):
    response = "You're looking at the loans of book %s."
    return HttpResponse(response % pk)
#TODO
def lend_book(request, pk):
    return HttpResponse("You're lending book %s." % pk)

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'library/authors.html'
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'library/author.html'
    paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='library/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan"""
    permission_required = 'library.can_see_borrowed'
    model = BookInstance
    template_name ='library/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('library.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            if request.user.has_perm('library.can_see_borrowed'):
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('library:loaned-book') )
            else:
                return HttpResponseRedirect(reverse('library:index'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'library/book_renew_librarian.html', context)

@login_required
@permission_required('library.can_mark_returned', raise_exception=True)
def renew_material_librarian(request, pk):
    """View function for renewing a specific MaterialInstance by librarian."""
    material_instance = get_object_or_404(MaterialInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewMaterialForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            material_instance.due_back = form.cleaned_data['renewal_date']
            material_instance.save()

            if request.user.has_perm('library.can_see_borrowed'):
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('library:loaned-material') )
            else:
                return HttpResponseRedirect(reverse('library:index'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': material_instance,
    }

    return render(request, 'library/material_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = "library.can_modify_author"
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "library.can_modify_author"
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "library.can_modify_author"
    model = Author
    success_url = reverse_lazy('library:authors')

class MaterialListView(generic.ListView):
    model = Material
    template_name = 'library/materials.html'
    paginate_by =10

class MaterialDetailView(generic.DetailView):
    model = Material
    template_name = 'library/material.html'

class BookInstanceDetailView(generic.DetailView):
    model = BookInstance
    template_name = 'library/bookInstance-detail.html'

class MaterialInstanceDetailView(generic.DetailView):
    model = MaterialInstance
    template_name = 'library/materialInstance-detail.html'

class OpeningHoursCreateView(CreateView):
    model = OpeningHours
    fields = ['weekday', 'to_hour', 'from_hour']

class OpeningHoursListView(generic.ListView):
    model = OpeningHours
    template_name = 'library/openinghours.html'
