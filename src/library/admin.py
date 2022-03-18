from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Book, Material, BookInstance, MaterialInstance, Genre, Author, Loan, Member, Language, Room, \
    LoanReminder

admin.site.register(Book)
admin.site.register(Material)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Room)
admin.site.register(LoanReminder)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ('label', 'book', 'status')
    list_filter = ('status',)

    fieldsets = (
        (None, {
            'fields': ('book', 'label', 'imprint')
        }),
        ('Availability', {
            'fields': ('status',)
        }),
    )


@admin.register(MaterialInstance)
class MaterialInstanceAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ('label', 'material', 'status')
    list_filter = ('status',)

    fieldsets = (
        (None, {
            'fields': ('material', 'label')
        }),
        ('Availability', {
            'fields': ('status',)
        }),
    )


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    search_fields = ['item__label']
    list_display = ('item', 'lent_on', 'due_back', 'last_reminder')
    # list_filter = ('returned','is_overdue')

    fieldsets = (
        (None, {
            'fields': ('item', 'borrower')
        }),
        ('Timeline', {
            'fields': ('lent_on', 'due_back', 'returned_on')
        }),
    )


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'members'


class TokenInline(admin.StackedInline):
    model = Token


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline, TokenInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
