from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from datetime import datetime, timedelta
from polymorphic.models import PolymorphicModel


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text=_('Enter a book genre (e.g. Science Fiction)'),
                            verbose_name=_('Name'))

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genre')


class Material(models.Model):
    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('library:material-detail', args=[str(self.id)])

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Materials')


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100, verbose_name=_('First name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of birth'))
    date_of_death = models.DateField(null=True, blank=True, verbose_name=_('Date of death'))

    def __str__(self):
        """String for representing the Model object."""
        if self.first_name != "":
            return f'{self.first_name} {self.last_name}'
        else:
            return self.last_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('library:author-detail', args=[str(self.id)])

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_modify_author", _("Can add, update or delete an author")),)
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Titel'))
    author = models.ManyToManyField(Author, help_text=_('Select the autor(s) of this book.'), verbose_name=_('Author'))
    genre = models.ManyToManyField(Genre, help_text=_('Select a genre for this book.'), blank=True, verbose_name=_('Genre'))
    summary = models.TextField(max_length=1000, help_text=_('Enter a brief description of the book.'), blank=True, verbose_name=_('Summary'))
    isbn = models.CharField(max_length=13, null=True, help_text=_('ISBN number (13 Characters)'), blank=True, verbose_name=_('ISBN'))
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Language'))

    def __str__(self):
        return f"{self.title} by {', '.join([str(author) for author in self.author.all()])}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('library:book-detail', args=[str(self.id)])

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text=_("Enter a natural languages name (e.g. English, French, Japanese etc.)."),
                            unique=True)

    languagecode = models.CharField(max_length=10,
                                    # Translators: This helptext includes an URL
                                    help_text=_(
                                        "Enter the language code for this language. For further information see  http://www.i18nguy.com/unicode/language-identifiers.html"),
                                    verbose_name=_('Language code'))

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    preferred_language = models.ForeignKey(Language, on_delete=models.PROTECT, null=True,
                                           verbose_name=_('Preferred language'))
    UID = models.CharField(max_length=50, blank=True, help_text=_("The UID of a NFC chip (e.g. in a student id)."),
                           verbose_name=_('UID'))

    @receiver(post_save, sender=User)
    def add_member(sender, instance, created, raw, using, **kwargs):
        if len(Member.objects.filter(user=instance)) != 1:
            Member.objects.create(user=instance)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("library:user-detail", args=[str(self.user.id)])

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')


class Item(PolymorphicModel):
    """Represents an item that is physically in the library"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text=_('Unique ID for this particular item across whole library.'),
                          verbose_name=_('Id'))
    label = models.CharField(max_length=20, unique=True, verbose_name=_('Label'))

    LOAN_STATUS = (
        ('m', _('Maintenance')),
        ('o', _('On loan')),
        ('a', _('Available')),
        ('r', _('Reserved')),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Item availability'),
    )

    class Meta:
        permissions = (("can_mark_returned", _("Set item as returned")),
                       ("can_see_borrowed", _("See all borrowed items")))
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return str(f"[{self.label}]")

    def borrow(self,
               borrower: Member,
               due_back=timezone.now() + timezone.timedelta(days=28),
               lent_on=timezone.now()):
        """
        Borrows the item by marking it as on loan and creating a loan

        Parameters
        ----------
        borrower:User The user that borrows the item
        due_back:datetime When the item has to be returned, default is one month later
        lent_on:datetime When the item was lent. Parameter most useful for testing

        Returns
        -------
        Loan: The created loan object
        """
        loan = Loan.objects.create(
            item=self,
            lent_on=lent_on,
            due_back=due_back,
            borrower=borrower,
        )
        loan.save()
        # Set status to on loan
        self.status = "o"
        self.save()
        return loan

    def return_item(self,
                    return_date=timezone.now()) -> bool:
        """
        Sets the item as available and mark the loan as returned

        The st
        Parameters
        ----------
        return_date:datetime=timezone.now()
            Defaults to now, but it is possible to use a custom return date (e.g. to avoid late fees when returned over weekend)

        Returns
        -------
        bool True if successful, else false
        """
        try:
            unreturned_loan_of_item = Loan.objects.filter(item=self,
                                                          returned_on=None)[0]
        except IndexError:
            return False
        unreturned_loan_of_item.returned_on = return_date
        unreturned_loan_of_item.save()
        # Set status to available
        self.status = "a"
        self.save()
        return True

    @property
    def borrower(self):
        """ Returns the current borrower or 'Not borrowed'"""
        try:
            last_loan = Loan.objects.filter(item=self).latest("lent_on")
            if last_loan.returned:
                raise Loan.DoesNotExist
            else:
                return last_loan.borrower
        except Loan.DoesNotExist:
            # Translators: Is shown instead of a person that borrowed the item
            return _("Not borrowed")

    @property
    def due_back(self):
        """ Returns the current due date or 'Not borrowed'"""
        try:
            last_loan = Loan.objects.filter(item=self).latest("lent_on")
            if last_loan.returned:
                raise Loan.DoesNotExist
            else:
                return last_loan.due_back
        except Loan.DoesNotExist:
            # Translators: Is shown instead of a person that borrowed the item
            return _("Not borrowed")

    @due_back.setter
    def due_back(self, value):
        """ Sets the due_back of the latest loan of the item to value'"""
        last_loan = Loan.objects.filter(item=self).latest("lent_on")
        last_loan.due_back = value

    @property
    def description(self) -> str:
        raise NotImplementedError


class BookInstance(Item):
    """Represents a copy of a book that is physically in the library"""

    def __str__(self):
        return f"[{self.label}] {self.book}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this bookInstance."""
        return reverse('library:bookInstance-detail', args=[str(self.id)])

    book = models.ForeignKey('Book', on_delete=models.RESTRICT, verbose_name=_('Book'))
    imprint = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Imprint'))

    class Meta:
        verbose_name = _('Book instance')
        verbose_name_plural = _('Book instances')

    @property
    def description(self) -> str:
        return str(self.book)


class MaterialInstance(Item):
    """Represents an instance of a material that is physically in the library"""

    def __str__(self):
        return f"[{self.label}] {self.material.name}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this materialInstance."""
        return reverse('library:materialInstance-detail', args=[str(self.id)])

    material = models.ForeignKey('Material', on_delete=models.RESTRICT, null=True, verbose_name=_('Material'))

    class Meta:
        verbose_name = _('Material instance')
        verbose_name_plural = _('Material instances')

    @property
    def description(self) -> str:
        return str(self.material)


class Loan(models.Model):
    borrower = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=_('Borrower'))
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name=_('Item'))
    lent_on = models.DateField(verbose_name=_('Lent on'))
    due_back = models.DateField(verbose_name=_('Due back'))
    returned_on = models.DateField(null=True, blank=True, verbose_name=_('Returned on'))

    def __str__(self):
        """String representation."""
        borrowed = _('borrowed until')
        return f"{self.item} {borrowed} {self.due_back}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this loan."""
        return reverse('library:loan-detail', args=[str(self.id)])

    def remind(self):
        LoanReminder.objects.create(loan=self, sent_on=timezone.now().date())

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    @property
    def returned(self):
        if self.returned_on:
            return True
        else:
            return False

    @property
    def last_reminder(self):
        try:
            return LoanReminder.objects.filter(loan=self).latest("sent_on").sent_on
        except LoanReminder.DoesNotExist:
            return self.lent_on

    @property
    def reminder_due(self):
        """True if a reminder is due, else false."""
        reminder_interval = 28
        days_since_last_reminder = datetime.now().date() - self.last_reminder
        return days_since_last_reminder >= timedelta(days=reminder_interval)

    @property
    def num_reminders(self):
        return len(LoanReminder.objects.filter(loan=self))

    class Meta:
        permissions = (('can_add_loan', _('Can add a loan for all user')),)
        verbose_name = _('Loan')
        verbose_name_plural = _('Loans')


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
    weekday = models.IntegerField(choices=WEEKDAYS, verbose_name=_('Weekday'))
    from_hour = models.TimeField(verbose_name=_('From hour'))
    to_hour = models.TimeField(verbose_name=_('To hour'))
    comment = models.CharField(max_length=200, blank=True, verbose_name=_('Comment'))

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')
        permissions = (('change_opening_hours', _('Can change opening hours')),)
        verbose_name = _('Opening hour')
        verbose_name_plural = _('Opening hours')

    def __str__(self):
        return f"{self.get_weekday_display()} {self.from_hour:%H:%M}-{self.to_hour:%H:%M}"


class LoanReminder(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, verbose_name=_('Loan'))
    sent_on = models.DateField(verbose_name=_('Sent on'))

    def __str__(self):
        return f"Reminder for {self.loan} sent on {self.sent_on}"

    class Meta:
        verbose_name = _('Loan Reminder')
        verbose_name_plural = _('Loan Reminders')


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_('Unique Id for this room'),
                          verbose_name=_('Id'))
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Name'))
    allowed_user = models.ManyToManyField(User, help_text=_("Users that are allowed to access this room."),
                                          verbose_name=_('Allowed user'))

    def __str__(self):
        return f"Room: {self.name}"

    def check_access(self, user):
        """ Check if the given user is allowed in the room"""
        return user in self.allowed_user.all()

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
