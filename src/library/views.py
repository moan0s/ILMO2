from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token

from django.contrib import messages

from .forms import RenewItemForm, UserSearchForm
from .models import Book, Author, BookInstance, Loan, Material, MaterialInstance, OpeningHours, Item, Member, \
    LoanReminder
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


def gather_metrics_data():
    """USERS"""
    num_user = User.objects.count()
    num_staff = User.objects.filter(is_staff=True).count()

    """ BOOKS """
    num_books = Book.objects.count()
    num_book_instances = BookInstance.objects.all().count()
    # Available books
    num_book_instances_available = BookInstance.objects.filter(status="a").count()

    """ Material """
    num_material = Material.objects.count()
    num_material_instances = MaterialInstance.objects.all().count()
    # Available materials
    num_material_instances_available = MaterialInstance.objects.filter(status="a").count()

    """ Authors """
    num_authors = Author.objects.count()

    """Loan"""
    num_loans = Loan.objects.count()
    num_unreturned_loans = Item.objects.filter(status="o").count()

    """Reminder"""
    reminder_sent_today = LoanReminder.objects.filter(sent_on=timezone.now().date()).count()

    data = {
        'users': num_user,
        'staff': num_staff,

        'books': num_books,
        'book_instances': num_book_instances,
        'book_instances_available': num_book_instances_available,

        'materials': num_material,
        'material_instances': num_material_instances,
        'material_instances_available': num_material_instances_available,

        'authors': num_authors,

        "loans": num_loans,
        "unreturned_loans": num_unreturned_loans,
        "reminder_sent_today": reminder_sent_today,
    }
    return data


def index(request):
    """View function for home page of site."""
    data = gather_metrics_data()
    context = data

    if request.user.is_staff:
        from .mail import MailReminder
        mail_reminder = MailReminder()
        mail_reminder.send()

    return render(request, 'library/index.html', context=context)


def metrics(request):
    data = gather_metrics_data()

    return JsonResponse(data)


def show_user(request, user, token=None):
    member = Member.objects.get(user=user)
    context = {"member": member,
               "token": token, }
    return render(request, 'library/member.html', context=context)


@login_required()
@permission_required("auth.user.view")
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return show_user(request, user)


@login_required()
def my_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)

    if request.method == 'POST':
        print(request.POST)
        if "create_token" in request.POST:
            print( _("Creating API token"))
            Token.objects.create(user=request.user)
        elif "delete_token" in request.POST:
            Token.objects.get(user=request.user).delete()
    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = None
    return show_user(request, user, token)

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'library/change_password.html'
    success_url = reverse_lazy("library:index")

class BookListView(generic.ListView):
    model = Book
    template_name = 'library/books.html'
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'library/book.html'


# TODO
def loans_of_book(request, pk):
    response = _("You're looking at the loans of book %s.")
    return HttpResponse(response % pk)


@login_required()
@permission_required("library.can_add_loan", raise_exception=True)
def borrow_item(request, pk):
    context = {}
    errors = ""
    item = get_object_or_404(Item, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UserSearchForm(request.POST)
        # Check if the form is valid:
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        queryset = User.objects.filter(Q(last_name__iexact=last_name) | Q(first_name__iexact=first_name))
        context['users'] = queryset
    # If this is a GET (or any other method) create the default form.
    else:
        form = UserSearchForm()

    context['form'] = form
    context['item'] = item

    return render(request, 'library/borrow-user-search.html', context=context)


@login_required()
@permission_required("library.can_add_loan", raise_exception=True)
def borrow_user(request, ik, uk):
    item = get_object_or_404(Item, pk=ik)
    user = get_object_or_404(User, pk=uk)

    item.borrow(borrower=Member.objects.get(user=user))
    loan = Loan.objects.filter(item=item).latest("lent_on")
    context = {"loan": loan}
    return render(request, 'library/loan-detail.html', context=context)


@login_required()
@permission_required("library.can_mark_returned", raise_exception=True)
def return_item(request, ik):
    item = get_object_or_404(Item, pk=ik)

    item.return_item()
    loan = Loan.objects.filter(item=item).latest("lent_on")
    context = {"loan": loan}
    return render(request, 'library/loan-detail.html', context=context)


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'library/authors.html'
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'library/author.html'
    paginate_by = 10


@login_required()
def list_loans_of_user(request):
    """View function for home page of site."""
    loans_by_user = Loan.objects.filter(borrower=Member.objects.get(user=request.user))
    returned_loans_by_user = [loan for loan in loans_by_user if (loan.returned)]
    unreturned_loans_by_user = [loan for loan in loans_by_user if not (loan.returned)]
    context = {
        'returned_loans': returned_loans_by_user,
        'unreturned_loans': unreturned_loans_by_user,
    }

    return render(request, 'library/list_loans_user.html', context=context)


@login_required()
@permission_required('library.can_see_borrowed', raise_exception=True)
def list_loans_unreturned(request):
    """View all unreturned items"""
    loans = Loan.objects.filter()
    unreturned_loans = [loan for loan in loans if not loan.returned]
    context = {
        'loan_list': unreturned_loans,
    }

    return render(request, 'library/list_loans.html', context=context)

@login_required()
@permission_required('library.can_see_borrowed', raise_exception=True)
def list_loans(request):
    """View all unreturned items"""
    loans = Loan.objects.all()
    context = {
        'loan_list': loans,
    }
    return render(request, 'library/list_loans.html', context=context)


@login_required
@permission_required('library.can_mark_returned', raise_exception=True)
def renew_item_librarian(request, pk):
    """View function for renewing a specific item by librarian."""
    item = get_object_or_404(Item, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewItemForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            item.due_back = form.cleaned_data['renewal_date']
            item.save()

            if request.user.has_perm('library.can_see_borrowed'):
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('library:index'))  # TOD: Redirect this to a loan overview
            else:
                return HttpResponseRedirect(reverse('library:index'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewItemForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'item': item,
    }

    return render(request, 'library/item_renew_librarian.html', context)


@login_required
def item_search(request):
    context = {}

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Check if the form is valid:
        q = request.POST['q']
        queryset = Item.objects.filter(Q(label__iexact=q))
        context['items'] = queryset

    return render(request, 'library/item-search.html', context=context)


def get_books(query):
    """Returns all book objects roughly matching the query"""
    books = Book.objects.filter(Q(title__icontains=query))
    return books


def get_book_intances(query):
    book_instances = BookInstance.objects.filter(Q(label__iexact=query))
    return book_instances


def get_material_instances(query):
    material_instances = MaterialInstance.objects.filter(Q(label__iexact=query) | Q(label__icontains=query))
    return material_instances


def get_materials(query):
    """Returns all material objects roughly matching the query"""
    materials = Material.objects.filter(Q(name__icontains=query))
    return materials


def get_user(query):
    user = []
    for search_string in query.split(" "):
        user.extend(User.objects.filter(
            Q(username__icontains=search_string) | Q(first_name__icontains=search_string) | Q(
                last_name__icontains=search_string)))
    return set(user)


def get_authors(query):
    authors = []
    for search_string in query.split(" "):
        authors.extend(Author.objects.filter(Q(first_name__icontains=search_string) | Q(
            last_name__icontains=search_string)))
    return set(authors)


def get_books_of_authors(authors):
    books = []
    for author in authors:
        books.extend(Book.objects.filter(author=author))
    return set(books)


def search(request):
    """
    Enables search for items and users for multiple fields
    """
    context = {}

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Check if the form is valid:
        q = request.POST['q']
        if request.user.has_perm('library.view_member'):
            context['user_list'] = get_user(q)

        books = []
        books.extend(get_books(q))
        authors = get_authors(q)
        books_by_author = get_books_of_authors(authors)
        books.extend(books_by_author)
        context['books'] = books
        context['materials'] = get_materials(q)
        context['book_instances'] = get_book_intances(q)
        context['material_instances'] = get_material_instances(q)

    return render(request, 'library/search.html', context=context)


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
    paginate_by = 10


class MaterialDetailView(generic.DetailView):
    model = Material
    template_name = 'library/material.html'


class BookInstanceDetailView(generic.DetailView):
    model = BookInstance
    template_name = 'library/bookInstance-detail.html'


class MaterialInstanceDetailView(generic.DetailView):
    model = MaterialInstance
    template_name = 'library/materialInstance-detail.html'


class LoanDetailView(generic.DetailView):
    model = Loan
    template_name = 'library/loan-detail.html'


class OpeningHoursCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.change_opening_hours"
    model = OpeningHours
    fields = ['weekday', 'from_hour', 'to_hour', 'comment']

    def get_success_url(self):
        return reverse('library:openinghours')


class OpeningHoursListView(generic.ListView):
    model = OpeningHours
    template_name = 'library/openinghours.html'


class OpeningHourDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.change_opening_hours"
    model = OpeningHours
    template_name = "library/openinghour_confirm_delete.html"
    success_url = reverse_lazy('library:openinghours')
